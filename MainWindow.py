from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, \
    QMainWindow, \
    QPushButton, \
    QWidget, \
    QVBoxLayout, \
    QLabel, \
    QHBoxLayout, \
    QListWidget, QListWidgetItem, QMenu, QGridLayout, QDialog
from PyQt6.QtGui import QPixmap, QAction
import sys

from MAPIKeyDialogWindow import MAPIKeyDialogWindow
from QRCodeDialog import QRCodeDialog
from computer import Computer
from CimputerInfoWindow import ComputerInfoWindow
import requests


def parse_all():
    all_comps_json = requests.get('http://46.151.30.76:5000/api/computers')
    list_of_dicts = all_comps_json.json()
    list_of_dicts = list_of_dicts['computers']
    list_of_comps = list()
    for el in list_of_dicts:
        tmp = Computer(**el)
        list_of_comps.append(tmp)
    return list_of_comps


class QCustomQWidget(QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.ComputerName = QLabel()
        self.ComputerStatus = QLabel()
        self.textQVBoxLayout.addWidget(self.ComputerName)
        self.textQVBoxLayout.addWidget(self.ComputerStatus)

        self.allQHBoxLayout = QHBoxLayout()
        self.comp_iconQLabel = QLabel()
        self.comp_iconQLabel.setMinimumSize(80, 80)
        self.comp_iconQLabel.setMaximumSize(80, 80)
        self.more_info_button = QPushButton("More info")
        self.more_info_button.clicked.connect(self.clicked)
        self.more_info_button.setFixedSize(100, 30)
        self.allQHBoxLayout.addWidget(self.comp_iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.allQHBoxLayout.addWidget(self.more_info_button, 2)
        self.setLayout(self.allQHBoxLayout)

    def setComputerName(self, text):
        self.ComputerName.setText(text)

    def setComputerStatus(self, text):
        self.ComputerStatus.setText(text)
        if (text == 'Active'):
            self.ComputerStatus.setStyleSheet('color: rgb(3, 192, 60);')
        else:
            self.ComputerStatus.setStyleSheet('color: rgb(255, 0, 0);')

    def setIcon(self):
        self.comp_iconQLabel.setPixmap(QPixmap('computer_icon.png'))

    def setButtonName(self, text):
        self.more_info_button.setObjectName(str(text))

    def clicked(self):
        sender = self.sender()
        self.window = ComputerInfoWindow(sender.objectName())
        self.window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.index = 0
        self._createMenuBar()
        self.list_of_comps = parse_all()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        computers_button = QPushButton("Computers")
        computers_button.setFixedSize(180, 40)
        computers_button.clicked.connect(self.clicked)

        users_button = QPushButton("AD Users")
        users_button.setFixedSize(180, 40)
        users_button.clicked.connect(self.clicked)

        keys_button = QPushButton("API Keys")
        keys_button.setFixedSize(180, 40)
        keys_button.clicked.connect(self.clicked)

        grid.addWidget(computers_button, 0, 0)
        grid.addWidget(users_button, 0, 1)
        grid.addWidget(keys_button, 0, 2)

        self.computersQListWidget = QListWidget()
        self.CreateComputerListWidget()
        grid.addWidget(self.computersQListWidget, 1, 0, 1, 3)

        self.setWindowTitle("InBetween")
        self.setMinimumSize(QSize(600, 600))

        centralWidget = QWidget()
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)

    def CreateComputerListWidget(self):
        self.fillComputerListWidget()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fillComputerListWidget)
        self.timer.start(100)


    def fillComputerListWidget(self):
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
        if self.index == len(self.list_of_comps):
            self.timer.stop()

    def _createMenuBar(self):
        self.all_menu = self.menuBar()
        mamangement_menu = QMenu("Management", self)
        self.all_menu.addMenu(mamangement_menu)
        actions_menu = self.all_menu.addMenu("Actions")
        self.all_menu.addMenu(actions_menu)

        NewMobileAPIAction = QAction('New mobile API key', self)
        NewMobileAPIAction.setStatusTip('Release new API key to connect mobile app')
        NewMobileAPIAction.triggered.connect(self.generateAPIKey)
        mamangement_menu.addAction(NewMobileAPIAction)

    def clicked(self):
        pass

    def generateAPIKey(self):
        dlg = MAPIKeyDialogWindow(self)
        dlg.setWindowTitle("New API Key Creation")
        if dlg.exec():
            dlg_qr = QRCodeDialog(self)
            dlg_qr.setWindowTitle("QRCode")
            dlg_qr.exec()
