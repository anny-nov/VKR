from datetime import datetime

import requests

from Log import Log
from APIKeyDialogWindow import fill_api_key
from main_code.Access import get_api_key

API_KEY = ''

class Chart():
    def __init__(self, hardware_id, start=0, finish=0):
        if start == 0:
            self.start = datetime(datetime.today())
            self.start = datetime.timestamp(self.start)
        else:
            self.start = start
        if finish == 0:
            self.finish = datetime.now()
            self.start = datetime.timestamp(self.start)
        else:
            self.finish = finish
        self.hardware_id = hardware_id

    def get_gata(self):
        global API_KEY
        API_KEY = get_api_key()
        api_url = 'http://afire.tech:5000/api/log?hardware_id=' + self.hardware_id + '&from=' + str(
            self.start) + '&to=' + str(self.finish) + '&type=1&api_key=' + API_KEY
        print(api_url)
        log_list_json = requests.get(api_url)
        log_list_dict = log_list_json.json()
        log_list_dict = log_list_dict['logs']
        self.cpus = list()
        self.rams = list()
        self.times = list()
        for el in log_list_dict:
            tmp = Log(**el)
            tmp.parse_time()
            tmp.get_load()
            self.cpus.append(tmp.cpu)
            self.rams.append(tmp.ram)
            self.times.append(tmp.timestamp)
        print(self.cpus)
        print(self.rams)
        print(self.times)
