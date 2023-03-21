from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, \
    QPushButton, \
    QWidget, \
    QLabel, \
    QListWidget, QListWidgetItem, QMenu, QGridLayout
from PyQt6.QtGui import QAction
import os

from APIKey import APIKey
from APIKeyCustomWidget import QKeyCustomQWidget
from ComputerCustomWidget import QCustomQWidget
from APIKeyDialogWindow import APIKeyDialogWindow
from QRCodeDialog import QRCodeDialog
from computer import Computer
from FirstAPIKeyDialogWindow import FirstAPIKeyDialogWindow
import requests

API_KEY = ''


def check_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    if len(key) == 0:
        dlg = FirstAPIKeyDialogWindow()
        dlg.setWindowTitle("First log in")
        dlg.exec()
    fill_api_key()

def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key


def parse_all():
    message = 'http://46.151.30.76:5000/api/computers' + '?api_key=' + API_KEY
    print(message)
    all_comps_json = requests.get(message)
    list_of_dicts = all_comps_json.json()
    print(list_of_dicts)
    list_of_dicts = list_of_dicts['computers']
    list_of_comps = list()
    for el in list_of_dicts:
        tmp = Computer(**el)
        list_of_comps.append(tmp)
    return list_of_comps


def parse_all_keys():
    all_keys_json = requests.get('http://46.151.30.76:5000/api/clients?api_key=' + API_KEY)
    list_of_dicts = all_keys_json.json()
    print(list_of_dicts)
    list_of_dicts = list_of_dicts['clients']
    list_of_keys = list()
    for el in list_of_dicts:
        tmp = APIKey(**el)
        list_of_keys.append(tmp)
    return list_of_keys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        check_api_key()
        self.index = 0
        self._createMenuBar()
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.CreateComputerListWidget()
        self.grid.addWidget(self.computersQListWidget, 1, 0, 1, 3)

        computers_button = QPushButton("Computers")
        computers_button.setFixedSize(180, 40)
        computers_button.clicked.connect(lambda: self.clicked('computers'))

        users_button = QPushButton("AD Users")
        users_button.setFixedSize(180, 40)
        users_button.clicked.connect(lambda: self.clicked('users'))

        keys_button = QPushButton("API Keys")
        keys_button.setFixedSize(180, 40)
        keys_button.clicked.connect(lambda: self.clicked('keys'))

        self.grid.addWidget(computers_button, 0, 0)
        self.grid.addWidget(users_button, 0, 1)
        self.grid.addWidget(keys_button, 0, 2)

        self.setWindowTitle("InBetween")
        self.setMinimumSize(QSize(600, 600))

        centralWidget = QWidget()
        centralWidget.setLayout(self.grid)
        self.setCentralWidget(centralWidget)

    def CreateComputerListWidget(self):
        self.computersQListWidget = QListWidget()
        self.list_of_comps = parse_all()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fillComputerListWidget)
        self.timer.start(50)

    def fillComputerListWidget(self):
        if self.index < len(self.list_of_comps):
            status = 'Active'
            compLineWidget = QCustomQWidget()
            compLineWidget.setComputerName(str(self.list_of_comps[self.index].name))
            compLineWidget.setComputerStatus(str(status))
            compLineWidget.setIcon()
            compLineWidget.setButtonName(self.list_of_comps[self.index].hardware_id)
            computersQListWidgetItem = QListWidgetItem(self.computersQListWidget)
            computersQListWidgetItem.setSizeHint(compLineWidget.sizeHint())
            self.computersQListWidget.addItem(computersQListWidgetItem)
            self.computersQListWidget.setItemWidget(computersQListWidgetItem, compLineWidget)
            self.index += 1

        if self.index >= len(self.list_of_comps):
            self.timer.stop()
            self.index = 0

    def _createMenuBar(self):
        self.all_menu = self.menuBar()
        mamangement_menu = QMenu("Management", self)
        self.all_menu.addMenu(mamangement_menu)
        actions_menu = self.all_menu.addMenu("Actions")
        self.all_menu.addMenu(actions_menu)

        NewMobileAPIAction = QAction('New API key', self)
        NewMobileAPIAction.setStatusTip('Release new API key to connect personal computer, server or mobile phone')
        NewMobileAPIAction.triggered.connect(self.new_APIKey)
        mamangement_menu.addAction(NewMobileAPIAction)

    def clicked(self, text):
        item = self.grid.itemAtPosition(1, 1)
        item.widget().deleteLater()
        match text:
            case 'computers':
                self.CreateComputerListWidget()
                self.grid.addWidget(self.computersQListWidget, 1, 0, 1, 3)
            case 'users':
                users_msg = QLabel("Here will be list of Windows Active Directory Users soon!")
                users_msg.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.grid.addWidget(users_msg, 1, 0, 1, 3)
            case 'keys':
                self.CreateAPIKeysListWidget()
                self.grid.addWidget(self.keysQListWidget, 1, 0, 1, 3)
            case _:
                error = QLabel("Something went wrong! Please try to click the button again!")
                error.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.grid.addWidget(error, 1, 0, 1, 3)

    def new_APIKey(self):
        dlg = APIKeyDialogWindow(self)
        dlg.setWindowTitle("New API Key Creation")
        if dlg.exec():
            dlg_qr = QRCodeDialog(self)
            dlg_qr.setWindowTitle("QRCode")
            if dlg_qr.exec():
                os.remove('api_key_qr.png')

    def CreateAPIKeysListWidget(self):
        self.keysQListWidget = QListWidget()
        self.list_of_keys = parse_all_keys()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fillAPIKeysListWidget)
        self.timer.start(50)

    def fillAPIKeysListWidget(self):
        if self.index < len(self.list_of_keys):
            keyLineWidget = QKeyCustomQWidget()
            keyLineWidget.setClientName(str(self.list_of_keys[self.index].name))
            keyLineWidget.setKeyType(str(self.list_of_keys[self.index].type))
            keyLineWidget.setButtonName(self.list_of_keys[self.index].id)
            keysQListWidgetItem = QListWidgetItem(self.keysQListWidget)
            keysQListWidgetItem.setSizeHint(keyLineWidget.sizeHint())
            self.keysQListWidget.addItem(keysQListWidgetItem)
            self.keysQListWidget.setItemWidget(keysQListWidgetItem, keyLineWidget)
            self.index += 1
        if self.index >= len(self.list_of_keys):
            self.timer.stop()
            self.index = 0