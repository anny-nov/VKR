import requests
from PyQt6.QtWidgets import QMainWindow

from main_code.Log import Log

API_KEY = ''

def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key

def parse_log(log_id, hardware_id):
    api_url = 'http://afire.tech:5000/api/log?hardware_id=' + hardware_id + '&id='\
              + str(log_id) + '&api_key=' + API_KEY
    print(api_url)
    log_json = requests.get(api_url)
    log_dict = log_json.json()
    log_dict = log_dict['logs']
    log = Log(**log_dict)
    return log

class LogInfo(QMainWindow):
    def __init__(self, object_id, hardware_id, parent=None):
        super(LogInfo, self).__init__(parent)
        fill_api_key()
        self.log = parse_log(object_id, hardware_id)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Log ' + str(self.log.id))