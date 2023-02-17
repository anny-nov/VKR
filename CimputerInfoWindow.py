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


def parse_from_json(hardware_id):
    api_url = 'http://46.151.30.76:5000/api/computer?hardware_id=' + hardware_id
    comp_json = requests.get(api_url)
    comp_dict = comp_json.json()
    comp_info = Computer(**comp_dict)
    return comp_info


class ComputerInfoWindow(QWidget):
    def __init__(self, hardware_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detailed information about computer")
        self.setMinimumSize(QSize(600, 600))

        comp_info = parse_from_json(hardware_id)
        print(comp_info.hardware_id, comp_info.name)
