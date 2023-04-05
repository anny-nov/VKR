import os

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, \
    QMainWindow, \
    QPushButton, \
    QWidget, \
    QLabel, \
    QListWidget, QListWidgetItem, QMenu, QGridLayout, QCheckBox
from PyQt6.QtGui import QPixmap, QAction, QFont
import sys

from APIKeyDialogWindow import APIKeyDialogWindow
from QRCodeDialog import QRCodeDialog
from computer import Computer
import requests

from main_code import menu
from main_code.APIKey import APIKey

API_KEY = ''


def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key

def parse_from_json(id):
    api_url = 'http://46.151.30.76:5000/api/client?id=' + id + '&api_key=' + API_KEY
    comp_json = requests.get(api_url)
    comp_dict = comp_json.json()
    comp_info = APIKey(**comp_dict)
    return comp_info


class KeyInfoWindow(QMainWindow):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        fill_api_key()
        self.key_info = parse_from_json(id)
        self.initUI()
        self._createMenuBar()

    def initUI(self):
        self.setWindowTitle('Client Information')
        self.layout = QGridLayout()
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.bold()
        qr_button = QPushButton('Show QR')
        self.settings_button = QPushButton('Change Settings')
        self.settings_button.clicked.connect(self.choose_settings)
        self.confirm_button = QPushButton('Confirm')
        self.confirm_button.clicked.connect(self.confirmed)
        client_name = QLabel(self.key_info.name)
        client_name.setFont(header_font)
        client_id = QLabel('ID: ' + str(self.key_info.id))
        client_type = QLabel('Type: ' + self.key_info.type)
        api_key = QLabel('API Key: ' + self.key_info.api_key)
        print(self.key_info.api_key)
        api_key.adjustSize()
        security_header = QLabel('Security Settings')
        security_font = QFont()
        security_font.bold()
        security_font.setPointSize(14)
        security_header.setFont(security_font)


        comps_label = QLabel("Computers")
        self.comp_read = QCheckBox("Read")
        self.comp_read.setDisabled(True)
        self.comp_update = QCheckBox("Update")
        self.comp_update.setDisabled(True)
        self.comp_add = QCheckBox("Add")
        self.comp_add.setDisabled(True)
        self.comp_delete = QCheckBox("Delete")
        self.comp_delete.setDisabled(True)

        client_label = QLabel("API Keys")
        self.client_read = QCheckBox("Read")
        self.client_read.setDisabled(True)
        self.client_update = QCheckBox("Update")
        self.client_update.setDisabled(True)
        self.client_add = QCheckBox("Add")
        self.client_add.setDisabled(True)
        self.client_delete = QCheckBox("Delete")
        self.client_delete.setDisabled(True)

        logs_label = QLabel("Logs")
        self.log_read = QCheckBox("Read")
        self.log_read.setDisabled(True)
        self.log_update = QCheckBox("Update")
        self.log_update.setDisabled(True)
        self.log_add = QCheckBox("Add")
        self.log_add.setDisabled(True)
        self.log_delete = QCheckBox("Delete")
        self.log_delete.setDisabled(True)

        checkbox_layout = QGridLayout()
        checkbox_layout.addWidget(comps_label, 0, 0)
        checkbox_layout.addWidget(client_label, 0, 1)
        checkbox_layout.addWidget(logs_label, 0, 2)
        checkbox_layout.addWidget(self.client_read, 1, 1)
        checkbox_layout.addWidget(self.client_update, 2, 1)
        checkbox_layout.addWidget(self.client_add, 3, 1)
        checkbox_layout.addWidget(self.client_delete, 4, 1)
        checkbox_layout.addWidget(self.comp_read, 1, 0)
        checkbox_layout.addWidget(self.comp_update, 2, 0)
        checkbox_layout.addWidget(self.comp_add, 3, 0)
        checkbox_layout.addWidget(self.comp_delete, 4, 0)
        checkbox_layout.addWidget(self.log_read, 1, 2)
        checkbox_layout.addWidget(self.log_update, 2, 2)
        checkbox_layout.addWidget(self.log_add, 3, 2)
        checkbox_layout.addWidget(self.log_delete, 4, 2)

        self.layout.addWidget(client_name, 0, 0)
        self.layout.addWidget(client_id, 1, 0)
        self.layout.addWidget(client_type, 2, 0)
        self.layout.addWidget(api_key, 3, 0)
        self.layout.addWidget(qr_button, 3, 1)
        self.layout.addWidget(security_header, 6, 0)
        self.layout.addWidget(self.settings_button, 6, 1)
        self.layout.addLayout(checkbox_layout, 7, 0, 1, 2)

        view = QWidget(self)
        self.setCentralWidget(view)
        view.setLayout(self.layout)

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

        DeleteAction = QAction('Delete API Key', self)
        DeleteAction.setStatusTip('Completely delete information about client from database')
        DeleteAction.triggered.connect(lambda: menu.DeleteAPIKey(self, self.key_info.id))
        actions_menu.addAction(DeleteAction)

    def choose_settings(self):
        self.layout.removeItem(self.settings_button)
        self.layout.addWidget(self.confirm_button, 6, 1)

    def confirmed(self):
        self.layout.removeItem(self.confirm_button)
        self.layout.addWidget(self.settings_button, 6, 1)