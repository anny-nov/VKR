import os

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, \
    QMainWindow, \
    QPushButton, \
    QWidget, \
    QLabel, \
    QListWidget, QListWidgetItem, QMenu, QGridLayout
from PyQt6.QtGui import QPixmap, QAction, QFont
import sys

from APIKeyDialogWindow import APIKeyDialogWindow
from QRCodeDialog import QRCodeDialog
from computer import Computer
import requests
from QTChat_copy import Chat_Widget
from main_code import menu
from main_code.Log import Log
from main_code.LogCustomWidget import LogCustomQWidget

API_KEY = ''

def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key

def parse_from_json(hardware_id):
    api_url = 'http://46.151.30.76:5000/api/computer?hardware_id=' + hardware_id + '&api_key=' + API_KEY
    comp_json = requests.get(api_url)
    comp_dict = comp_json.json()
    comp_info = Computer(**comp_dict)
    return comp_info

def parse_log(hardware_id):
    api_url = 'http://afire.tech:5000/api/log?hardware_id=' + hardware_id + '&api_key=' + API_KEY
    log_list_json = requests.get(api_url)
    log_list_dict = log_list_json.json()
    log_list_dict = log_list_dict['logs']
    log_list = list()
    for el in log_list_dict:
        tmp = Log(**el)
        tmp.parse_data()
        tmp.parse_time()
        log_list.append(tmp)
    return log_list


class ComputerInfoWindow(QMainWindow):
    def __init__(self, hardware_id, parent=None):
        super().__init__(parent)
        fill_api_key()
        self.comp_info = parse_from_json(hardware_id)
        self.logs = parse_log(hardware_id)
        print(self.logs)
        self.initUI()
        self._createMenuBar()
        self.index = 0

    def initUI(self):
        self.setWindowTitle("Detailed information about computer")
        self.setMinimumSize(QSize(600, 600))
        self.grid = QGridLayout()

        ComputerName = QLabel(self.comp_info.name)
        font = QFont()
        font.setPointSize(14)
        ComputerName.setFont(font)
        ComputerId = QLabel('Hardware ID: ' + self.comp_info.hardware_id)
        CpuInfo = QLabel('CPU: ' + self.comp_info.cpu)
        OSInfo = QLabel('OS: ' + self.comp_info.OS)
        DisksHeader = QLabel('Hard disks: ')
        Gpusheader = QLabel('GPUs: ')
        ChartsHeader = QLabel('Metriks of computer')
        ChartsHeader.setFont(font)
        headers_font = QFont()
        headers_font.setPointSize(14)
        DisksHeader.setFont(headers_font)
        Gpusheader.setFont(headers_font)

        disks_list = QListWidget()
        disks_list.setMaximumSize(400,100)
        gpus_list = QListWidget()
        gpus_list.setMaximumSize(400,100)
        for el in self.comp_info.disks:
            disks_list.addItem(el)
        for el in self.comp_info.gpus:
            gpus_list.addItem(el)


        #temp_chat = QLabel('There will be chat soon')
        chat_class = Chat_Widget()
        chat = chat_class.initLayout()
        #temp_logs = QLabel('There will be logs soon')
        self.CreateLogListWidget()
        temp_chart = QLabel('There will be charts soon')


        self.grid.addWidget(self.logListWidget, 0, 0, 5, 2)
        self.grid.addLayout(chat, 6, 0, 5, 2)
        self.grid.addWidget(ComputerName, 0, 3, 1, 2)
        self.grid.addWidget(ComputerId, 1, 3, 1, 2)
        self.grid.addWidget(OSInfo, 2, 3, 1, 2)
        self.grid.addWidget(CpuInfo, 3, 3, 1, 2)
        self.grid.addWidget(DisksHeader, 4, 3, 1, 2)
        self.grid.addWidget(disks_list, 5, 3, 1, 2)
        self.grid.addWidget(Gpusheader, 6, 3, 1, 2)
        self.grid.addWidget(gpus_list, 7, 3, 1, 2)
        self.grid.addWidget(ChartsHeader, 8, 3, 1, 2)
        self.grid.addWidget(temp_chart, 9, 3, 1, 2)

        view = QWidget(self)
        self.setCentralWidget(view)
        view.setLayout(self.grid)

    def _createMenuBar(self):
        self.all_menu = self.menuBar()
        mamangement_menu = QMenu("Management", self)
        self.all_menu.addMenu(mamangement_menu)
        actions_menu = self.all_menu.addMenu("Actions")
        self.all_menu.addMenu(actions_menu)

        NewMobileAPIAction = QAction('New mobile API key', self)
        NewMobileAPIAction.setStatusTip('Release new API key to connect mobile app')
        NewMobileAPIAction.triggered.connect(menu.new_APIKey)
        mamangement_menu.addAction(NewMobileAPIAction)

        DeleteAction = QAction('Delete computer', self)
        DeleteAction.setStatusTip('Completely delete information about computer from database')
        DeleteAction.triggered.connect(lambda: menu.DeleteComputer(self, self.comp_info.hardware_id))
        actions_menu.addAction(DeleteAction)

    def CreateLogListWidget(self):
        self.logListWidget = QListWidget()
        self.logs = parse_log(self.comp_info.hardware_id)
        self.timer = QTimer()
        self.timer.timeout.connect(self.fillLogListWidget)
        self.timer.start(50)

    def fillLogListWidget(self):
        if self.index < len(self.logs):
            LogLineWidget = LogCustomQWidget()
            LogLineWidget.setText(str(self.logs[self.index].data))
            LogLineWidget.setTime(str(self.logs[self.index].datetime))
            LogLineWidget.setIcon(self.logs[self.index].type)
            LogLineWidget.setId(self.logs[self.index].id)
            logListWidgetItem = QListWidgetItem(self.logListWidget)
            logListWidgetItem.setSizeHint(LogLineWidget.sizeHint())
            self.logListWidget.addItem(logListWidgetItem)
            self.logListWidget.setItemWidget(logListWidgetItem, LogLineWidget)
            self.index += 1
        if self.index >= len(self.logs):
            self.timer.stop()
            self.index = 0
