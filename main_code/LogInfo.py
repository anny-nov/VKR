import requests
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget

from main_code.Log import Log

API_KEY = ''

def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key

def parse_log(log_id, hardware_id):
    api_url = 'http://afire.tech:5000/api/log?hardware_id=' + hardware_id + '&api_key=' + API_KEY
    print(log_id)
    log = None
    log_json = requests.get(api_url)
    log_list_dict = log_json.json()
    log_list_dict = log_list_dict['logs']
    for el in log_list_dict:
        tmp = Log(**el)
        if tmp.id == log_id:
            tmp.parse_time()
            log = tmp
    return log

class LogInfo(QMainWindow):
    def __init__(self, object_id, hardware_id, parent=None):
        super(LogInfo, self).__init__(parent)
        fill_api_key()
        self.log = parse_log(object_id, hardware_id)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Log ' + str(self.log.id))
        self.layout = QVBoxLayout()
        header = QLabel('Log ' + str(self.log.id))
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.bold()
        header.setFont(header_font)
        log_time = QLabel(str(self.log.datetime))
        log_info = QLabel(str(self.log.data))
        log_info.setWordWrap(True)
        self.layout.addWidget(header)
        self.layout.addWidget(log_time)
        self.layout.addWidget(log_info)
        view = QWidget(self)
        self.setCentralWidget(view)
        view.setLayout(self.layout)
