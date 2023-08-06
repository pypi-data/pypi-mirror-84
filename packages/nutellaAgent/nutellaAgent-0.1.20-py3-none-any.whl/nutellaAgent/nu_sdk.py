import threading
import psutil
import asyncio
import json
import string
from .nu_requests import Requests

class Nutella(threading.Thread):

    def __init__(self):
        self.basic_info = dict() # run의 기본 정보
        self.config_info = dict() # run의 configuration 정보
        self.system_info = dict() # run의 system 정보
        self.metrics_info = dict() # run의 지표 정보 (시각화를 위한)
        self.psValue = psutil.Process() # ?
        self.request_url = "http://localhost:7000/admin/sdk"


    def init(self, run_name = None, project_key = None, reinit = False):
        project_id = asyncio.run(Requests().get_action(parameter = project_key, url = self.request_url))
        if not project_id:
            print("Error! The project doesn't exist")
        else:
            self.basic_info["run_name"] = run_name
            self.basic_info["project_key"] = project_key
            self.basic_info["project_id"] = project_id[0]["projectId"]
            # run_name으로 새로운 run 만드는 api를 위한 거 추가                
    
    def config(self, **config_datas):
        for key, value in config_datas.items():
            self.config_info[key] = value
        asyncio.run(Requests().post_action(request_datas = self.config_info, url = self.request_url))

    def log(self, **metrics_datas):
        self.metrics_info["run_name"] = self.basic_info["run_name"]

        for key, value in metrics_datas.items():
            self.metrics_info[key] = value
        asyncio.run(Requests().post_action(request_datas = self.metrics_info, url = self.request_url))

    def hardware_system_value(self):
        p = psutil.Process()
        self.system_info["cpu"]=min(65535, int(((p.cpu_percent(interval=None) / 100) / psutil.cpu_count(False)) * 65535))
        self.system_info["memory"]= min(65535, int((p.memory_percent() / 100) * 65535))
        self.system_info["net"]=psutil.net_io_counters()
        self.system_info["disk"]=psutil.disk_io_counters()

    def setrequest_url(self, url):
        self.request_url = url