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
        pass

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