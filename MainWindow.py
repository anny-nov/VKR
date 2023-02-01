from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, \
    QMainWindow, \
    QPushButton, \
    QWidget, \
    QVBoxLayout, \
    QLabel, \
    QHBoxLayout, \
    QListWidget, QListWidgetItem
from PyQt6.QtGui import QPixmap
import sys
from computer import Computer
import requests


def parse_all():
    all_comps_json = requests.get('http://46.151.30.76:5000/api/computers')
    list_of_dicts = all_comps_json.json()
    list_of_dicts = list_of_dicts['computers']
    list_of_comps = list()
    for el in list_of_dicts:
        tmp = Computer(el)
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
        self.allQHBoxLayout.addWidget(self.comp_iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InBetween")
        self.setMinimumSize(QSize(600, 600))
        self.list_of_comps = parse_all()
        for comp in self.list_of_comps:
            pass
        self.index = 0
        self.computersQListWidget = QListWidget(self)
        self.setCentralWidget(self.computersQListWidget)
        self.fillListWidget()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fillListWidget)
        self.timer.start(100)

    def fillListWidget(self):
        status = 'Active'
        compLineWidget = QCustomQWidget()
        compLineWidget.setComputerName(str(self.list_of_comps[self.index].name))
        compLineWidget.setComputerStatus(str(status))
        compLineWidget.setIcon()
        computersQListWidgetItem = QListWidgetItem(self.computersQListWidget)
        computersQListWidgetItem.setSizeHint(compLineWidget.sizeHint())
        self.computersQListWidget.addItem(computersQListWidgetItem)
        self.computersQListWidget.setItemWidget(computersQListWidgetItem, compLineWidget)

        self.index += 1
        if self.index == len(self.list_of_comps):
            self.timer.stop()
