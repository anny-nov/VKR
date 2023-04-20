from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import ctypes
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from qtpy import QtWidgets, QtCore, QtGui, uic
import os
import socketio
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QLabel, QWidget, QTextEdit, QVBoxLayout, QScrollArea, QPushButton

import os
import base64
from io import BytesIO
from PIL import Image
from qtpy import QtWidgets, QtGui, QtCore
import json

from msg_json import serialize_message
from msg_json import deserialize_message
from msg_json import deserialize_history


class Ui_MainWindow(QWidget): #object
    #def setupUi(self, MainWindow):
    def __init__(self, chat_info, sio):
        super().__init__()
        self.chat_info = chat_info
        self.sio = sio

        self.chat_layout = QGridLayout()
        self.chat_layout.setSpacing(10)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.chat_layout)
        self.setWindowTitle("Chat")
        self.resize(640, 500)

        # Create the widgets
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 620, 400))
        self.textEdit.setReadOnly(True)
#
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(10, 420, 500, 30))

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(520, 420, 110, 30))
        self.pushButton.setText("Send")

        self.pushButton.clicked.connect(lambda: self.send_message(self.lineEdit.text(), self.sio, self.chat_info.get("room", "")))



    def show_msg(self, message):
        self.lineEdit.setText("")
        self.textEdit.append(f"{message.get('from','')} ({message.get('timestamp', '')}):       {message.get('msg', '')}")


    def send_message(self, msg, sio, room):
        # Read the message from the QLineEdit widget
        # Serialize the message to JSON and send it to the server
        _from = "2"
        #print("room   ", room)
        message = serialize_message(_from, room, msg)
        if msg:
            sio.emit('chat_message', json.dumps(message))

            # Clear the QLineEdit widget
            self.show_msg(message)


    def receive_message(self, data):
        # Parse the JSON message and extract the relevant fields
        # message_data = data['data']
        # sender = 'Server'
        # message = message_data['message']
        # time = message_data['time']
        # self.textEdit.append(f"{sender} ({time}):       {message}")
        message = deserialize_message(data)
        self.show_msg(message)

    def append_history(self, data):
        print(data)
        history = deserialize_history(data)
        array = history.get("messages", "")
        #array.reverse()
        for i in array:
            self.show_msg(i)




   #def send_message(self):
   #    # Read the message from the QLineEdit widget
   #    msg = self.lineEdit.text()

   #    # Serialize the message to JSON and send it to the server
   #    if msg:
   #        _from = "1"
   #        message = jsonHandler.serialize_message(_from, self.chat_info.get("room", ""), msg)
   #        self.sio.emit('chat_message', message)

   #        # Clear the QLineEdit widget
   #        self.lineEdit.setText("")
   #        self.textEdit.append(f"{_from} ({time}):       {msg}")



#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    #MainWindow = QtWidgets.QMainWindow()
#    ui = Ui_MainWindow()
#    #ui.setupUi(MainWindow)
#    #MainWindow.show()
#    ui.show()
#    sys.exit(app.exec_())