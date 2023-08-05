"""LocalWebServer API"""
import requests
from flask_restful import Resource
from flask import request
import glob
import os
from shutil import copy2
import json
from .args import Args
from .task_runner import Task, StationTask
import threading
from .utils import SingletonMeta, locked
from flask_restful import Api
import logging
from .ssh import SSHClient
import time


class LocalWebServerAPI(Api):
    def __init__(self, prefix=Args().api_prefix, *args, **kwargs):
        super(LocalWebServerAPI, self).__init__(*args, prefix=prefix, **kwargs)
        self.add_resource(TaskFunction, '/<int:station>/<string:action>')
        self.add_resource(CheckFunction, '/check')
        self.add_resource(PauseFunction, '/pause')
        self.add_resource(ResumeFunction, '/resume')
        self.add_resource(LogFunction, '/log')


class LogFunction(Resource):
    lock = threading.Lock()
    
    def post(self):
        try:
            s = request.data.decode('utf-8')
        except UnicodeDecodeError:
            s = request.get_data(as_text=True)
        logging.getLogger().info(s)


class TaskFunction(Resource):
    def get(self, station, action):
        try:
            t = Task(station, action)
            t.start()
        except (Task.TaskRunningException, KeyError) as e:
            logging.getLogger().info(e)
            return {
                       "status": "failed",
                       "message": str(e)
            }, 422
        else:
            CheckFunction.bak({})
            return {"status": False, "message": "Started {}".format(t)}, 201


class BarcodeSingleton(str, metaclass=SingletonMeta):
    lock = threading.Lock()
    valid = True


class CheckFunction(Resource):
    bak_lock = threading.Lock()
    _bak = {}
    
    @property
    def logger(self) -> logging.getLoggerClass():
        return logging.getLogger(type(self).__name__)
    
    @classmethod
    @locked(bak_lock)
    def bak(cls, value=None):
        if value is not None:
            cls._bak = value
        return cls._bak
    
    log_endpoint = "http://{}:8080/log".format(Args().ip)
    
    def get(self):
        with Task.lock:
            task_running = Task.running
            task_type = Task.type
            task_str = str(Task._running)
        if task_running:
            self.logger.debug("{} is running".format(task_str))
            if issubclass(task_type, StationTask):
                with BarcodeSingleton.lock:
                    try:
                        rv = requests.get(self.log_endpoint)
                    except requests.exceptions.ConnectionError:
                        self.logger.info("{} - Connection Error".format(self.log_endpoint))
                    else:
                        self.logger.info("{} - Status Code {}".format(self.log_endpoint, rv.status_code))
                        self.logger.debug(rv.content.decode('ascii'))
                        if rv.status_code == 200:
                            CheckFunction.bak(rv.json())
                    finally:
                        output = CheckFunction.bak()
                    if BarcodeSingleton.valid and output.get("external", False):
                        self.logger.debug("Barcode is valid and stage is external")
                        while not BarcodeSingleton():
                            BarcodeSingleton.reset(requests.get("http://127.0.0.1:{}/exit".format(Args().barcode_port)).content.decode('ascii'))
                    if not BarcodeSingleton.valid and not output.get("external", True):
                        self.logger.debug("Barcode is not valid and stage is internal. Resetting barcode")
                        BarcodeSingleton.reset()
                        BarcodeSingleton.valid = True
                return {
                           "status": False,
                           "res": "Status: {}\nStage: {}{}".format(
                               output.get("status", None),
                               output.get("stage", None),
                               "\n\n{}".format(output["msg"]) if output.get("msg", None) else ""
                           )
                       }, 200
            else:
                return {"status": False, "res": task_str}, 200
        else:
            self.logger.debug("No task is running")
            with Task.lock:
                code = Task.exit_code
                Task.exit_code = None
            if code is None:
                # No station protocol was running, look for PCR result files
                pcr_result_files = sorted(glob.glob(Args().pcr_results), key=os.path.getctime, reverse=True)
                if pcr_result_files:
                    self.logger.debug("Found PCR files")
                    try:
                        with open(str(pcr_result_files[0]), 'r', encoding='utf-8-sig') as f:
                            result = json.load(f)
                    except Exception as e:
                        return {"status": True, "res": str(e)}, 500
                    # Make a backup of the PCR results
                    os.makedirs(Args().pcr_backup, exist_ok=True)
                    copy2(pcr_result_files[0], Args().pcr_backup)
                    # Delete the last file in order to not create confusion
                    os.remove(pcr_result_files[0])
                    return {"status": True, "res": result}, 200
                else:
                    self.logger.debug("No Protocol nor Result available")
                    return {"status": True, "res": "No Protocol nor Result available"}, 200
            else:
                # Station protocol has just ended, reset backup
                res = "Failed" if code else "Completed"
                self.logger.info("Protocol {}: exit code {}".format(res.lower(), code))
                if Args().log_local:
                    log_remote = CheckFunction.bak().get("runlog", None)
                    log_local = Args().log_local.format(time.strftime("%Y_%m_%d__%H_%M_%S"))
                    if log_remote:
                        os.makedirs(os.path.dirname(log_local), exist_ok=True)
                        try:
                            with SSHClient() as client:
                                with client.scp_client() as scp_client:
                                    scp_client.get(log_remote, log_local)
                        except Exception as e:
                            self.logger.warning("Could not copy runlog from '{}' to '{}':\n{}".format(log_remote, log_local, e))
                        else:
                            self.logger.info("Copied runlog from '{}' to '{}'".format(log_remote, log_local))
                CheckFunction.bak({})
                return {"status": True, "res": res, "exit_code": code}, 500 if code else 200


class PauseFunction(Resource):
    def get(self):
        try:
            requests.get("http://{}:8080/pause".format(Args().ip))
        except Exception as e:
            r = {"status": False, "res": str(e)}, 500
        else:
            r = {"status": False, "res": "Pausa"}, 200
        return r


class ResumeFunction(Resource):
    @staticmethod
    def _resume():
        try:
            requests.get("http://{}:8080/resume".format(Args().ip))
        except Exception as e:
            r = {"status": False, "res": str(e)}, 500
        else:
            r = {"status": False, "res": "Resumed"}, 200
        return r
    
    @locked(BarcodeSingleton.lock)
    def get(self):
        if BarcodeSingleton() and BarcodeSingleton.valid:
            try:
                while requests.get("http://127.0.0.1:{}/enter".format(Args().barcode_port)).content.decode('ascii') != BarcodeSingleton():
                    pass
            except Exception as e:
                r = {"status": False, "res": str(e)}, 500
            else:
                r = self._resume()
                BarcodeSingleton.valid = False
        else:
            r = self._resume()
        return r
        

# Copyright (c) 2020 Covmatic.
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
