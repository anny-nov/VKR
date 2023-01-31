from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
from computer import Computer
import requests

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InBetween")

        all_comps_json = requests.get('http://46.151.30.76:5000/api/computers')
        list_of_dicts = all_comps_json.json()
        list_of_dicts=list_of_dicts['computers']
        list_of_comps = list()
        for el in list_of_dicts:
            tmp = Computer(el)
            list_of_comps.append(tmp)

        button = QPushButton("Press Me!")
        self.setCentralWidget(button)