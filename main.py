from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
import requests
from computer import Computer
from MainWindow import MainWindow

app = QApplication(sys.argv)

print()

comp_json = requests.get('http://46.151.30.76:5000/api/computer?hardware_id=23523532gdfg534645')
comp_dict = comp_json.json()
print(comp_dict)

window = MainWindow()
window.show()

app.exec()
