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
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QLabel, QWidget

import os
import base64
from io import BytesIO
from PIL import Image
from qtpy import QtWidgets, QtGui, QtCore


# Create a SocketIO instance and connect to the chat server
sio = socketio.Client()
sio.connect('http://46.151.30.76:5000?api_key=AvIRCSEqgPxoUK8uUqaatQ')

class Chat_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initLayout()

    def initLayout(self):
        chat_layout = QGridLayout()
        chat_layout.setSpacing(10)

        self.textEdit = QtWidgets.QTextEdit(self)
        #self.textEdit.setGeometry(QtCore.QRect(10, 10, 300, 400))
        self.textEdit.setReadOnly(True)

        self.lineEdit = QtWidgets.QLineEdit(self)
        #self.lineEdit.setGeometry(QtCore.QRect(10, 420, 500, 30))

        self.pushButton = QtWidgets.QPushButton(self)
        #self.pushButton.setGeometry(QtCore.QRect(520, 420, 110, 30))
        self.pushButton.setText("Send")

        self.send_file_button = QtWidgets.QPushButton(self)
        #self.send_file_button.setGeometry(QtCore.QRect(520, 460, 110, 30))
        self.send_file_button.setText("Send File")

        self.pushButton.clicked.connect(self.send_message)
        self.send_file_button.clicked.connect(self.send_file)
        sio.on('my_response', self.receive_message)
        sio.on('my_response1', self.exe_status)

        self.image_button = QtWidgets.QPushButton(self)
        #self.image_button.setGeometry(QtCore.QRect(520, 500, 110, 30))
        self.image_button.setText("Send Image")
        self.image_label = QtWidgets.QLabel(self)
        #self.image_label.setGeometry(15,15,300,300)
        self.image_button.clicked.connect(self.send_image)
        sio.on('my_response1', self.receive_image)

        chat_layout.addWidget(self.textEdit)
        chat_layout.addWidget(self.lineEdit)
        return chat_layout

    def send_file(self):

        # open file explorer dialog and get selected file path
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a file to send", ".", "All files (*)")

        if file_path:
            # read file data and send it over SocketIO
            with open(file_path, 'rb') as f:
                data = f.read()
                sio.emit('my_event', data)

            # send status message to chat window
            json_message = {
                'from': 'ICO_Dima',
                'message': f"Sent file: {file_path}",
                'time': datetime.datetime.now().strftime("%D  %H:%M:%S"),
            }
            sio.emit('my_event', json_message)
        else:
            # send status message to chat window
            json_message = {
                'from': 'ICO_Dima',
                'message': 'File selection canceled',
                'time': datetime.datetime.now().strftime("%D  %H:%M:%S"),
            }
            sio.emit('my_event', json_message)

    def send_message(self):
        # Read the message from the QLineEdit widget
        message = self.lineEdit.text()

        # Serialize the message to JSON and send it to the server
        if message:
            json_message = {
                'from': 'ICO_Dima',
                'message': message,
                'time': datetime.datetime.now().strftime("%D  %H:%M:%S"),
            }
            sio.emit('my_event', json_message)

            # Clear the QLineEdit widget
            self.lineEdit.setText("")
            self.textEdit.append(f"{json_message['from']} ({json_message['time']}):       {json_message['message']}")

    def receive_message(self, data):
        # Parse the JSON message and extract the relevant fields
        message_data = data['data']
        sender = 'Server'
        message = message_data['message']
        time = message_data['time']
        self.textEdit.append(f"{sender} ({time}):       {message}")
        print(data)

    def exe_status(self, data):
        # Parse the JSON message and extract the relevant fields
        message_data = data['data']
        message = message_data['message']
        self.textEdit.append(f"{message}")
        print(data)

    def send_image(self):
        # Open a file dialog to choose an image file and send it to the server
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open Image', ".",'Image Files (*.png *.jpg *.jpeg *.gif)')
        if filename:
            with open(filename, 'rb') as f:
                image_data = f.read()
            sio.emit('my_event', {'username': "Dima", 'image_data': base64.b64encode(image_data).decode()})

    def receive_image(self, data):
        # Receive an image from the server and display it in the chat box
        message_data = data['data']
        image_data = base64.b64decode(message_data['image_data'])
        pixmap = QtGui.QPixmap.fromImage(QImage.fromData(image_data))
        scaled_pixmap = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
