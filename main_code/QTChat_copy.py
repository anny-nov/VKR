import datetime

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QImage
import socketio
from PyQt6.QtWidgets import QFileDialog, QGridLayout, QLabel, QWidget, QMainWindow, QVBoxLayout, QListWidget, \
    QListWidgetItem

import base64
from PyQt6 import QtWidgets, QtGui, QtCore

API_KEY = ''

def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key

# Create a SocketIO instance and connect to the chat server


class Chat_Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        fill_api_key()
        self.sio = socketio.Client()
        self.sio.connect('http://46.151.30.76:5000?api_key=' + API_KEY)

    def initLayout(self):
        chat_layout = QGridLayout()
        chat_layout.setSpacing(10)

        #self.textEdit = QtWidgets.QTextEdit(self)
        #self.textEdit.setReadOnly(True)
        self.message_history_widget=QWidget(self)
        self.message_history_widget.setStyleSheet("background-color:white;")
        self.message_history_widget.setMinimumSize(100, 200)
        layout = QVBoxLayout()
        self.message_history_widget.setLayout(layout)
        self.message_history = QListWidget(self.message_history_widget)
        self.message_history.setWordWrap(True)
        self.message_history_widget.layout().addWidget(self.message_history)

        self.lineEdit = QtWidgets.QLineEdit(self)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText("Send")

        self.send_file_button = QtWidgets.QPushButton(self)
        self.send_file_button.setText("Send File")

        self.pushButton.clicked.connect(self.send_message)
        self.send_file_button.clicked.connect(self.send_file)
        self.sio.on('my_response', self.receive_message)
        self.sio.on('my_response1', self.exe_status)

        self.image_button = QtWidgets.QPushButton(self)
        self.image_button.setText("Send Image")
        self.image_button.clicked.connect(self.send_image)
        self.sio.on('my_response1', self.receive_image)

        chat_layout.setColumnStretch(0, 10)
        chat_layout.addWidget(self.message_history_widget, 0, 0, 1, 2)
        chat_layout.addWidget(self.lineEdit, 1, 0, 1, 1)
        chat_layout.addWidget(self.pushButton, 1, 1, 1, 1)
        chat_layout.addWidget(self.image_button, 2, 1, 1, 1)
        chat_layout.addWidget(self.send_file_button, 3, 1, 1, 1)
        return chat_layout

    def send_file(self):

        # open file explorer dialog and get selected file path
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a file to send", ".", "All files (*)")

        if file_path:
            # read file data and send it over SocketIO
            with open(file_path, 'rb') as f:
                data = f.read()
                self.sio.emit('my_event', data)

            # send status message to chat window
            json_message = {
                'from': 'ICO_Dima',
                'message': f"Sent file: {file_path}",
                'time': datetime.datetime.now().strftime("%D  %H:%M:%S"),
            }
            self.sio.emit('my_event', json_message)
        else:
            # send status message to chat window
            json_message = {
                'from': 'ICO_Dima',
                'message': 'File selection canceled',
                'time': datetime.datetime.now().strftime("%D  %H:%M:%S"),
            }
            self.sio.emit('my_event', json_message)

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
            self.sio.emit('my_event', json_message)

            # Clear the QLineEdit widget
            self.lineEdit.setText("")
            msg = QLabel(f"{json_message['from']} ({json_message['time']}):       {json_message['message']}")
            msg.setMaximumWidth(self.message_history_widget.width())
            msg.setWordWrap(True)
            self.message_history.addItem(f"{json_message['from']} ({json_message['time']}):       {json_message['message']}")
            #self.textEdit.append(msg)

    def receive_message(self, data):
        print(data)
        # Parse the JSON message and extract the relevant fields
        message_data = data['data']
        sender = 'Server'
        message = message_data['message']
        time = message_data['time']
        msg = QLabel(f"{sender} ({time}):       {message}")
        list_item = QListWidgetItem(msg)
        self.message_history.addItem(list_item)
        #self.textEdit.append(f"{sender} ({time}):       {message}")
        print(data)

    def exe_status(self, data):
        # Parse the JSON message and extract the relevant fields
        message_data = data['data']
        message = message_data['message']
        msg = QLabel(f"{message}")
        list_item = QListWidgetItem(msg)
        self.message_history.addItem(list_item)
        #self.textEdit.append(f"{message}")
        print(data)

    def send_image(self):
        # Open a file dialog to choose an image file and send it to the server
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open Image', ".",
                                                            'Image Files (*.png *.jpg *.jpeg *.gif)')
        if filename:
            with open(filename, 'rb') as f:
                image_data = f.read()
            self.sio.emit('my_event', {'username': "Dima", 'image_data': base64.b64encode(image_data).decode()})

    def receive_image(self, data):
        # Receive an image from the server and display it in the chat box
        message_data = data['data']
        image_data = base64.b64decode(message_data['image_data'])
        pixmap = QtGui.QPixmap.fromImage(QImage.fromData(image_data))
        scaled_pixmap = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        msg = QLabel(f"{message_data}")
        list_item = QListWidgetItem(msg)
        self.message_history.addItem(list_item)
        list_item = QListWidgetItem(image_label)
        self.message_history.addItem(list_item)


    def mouseDoubleClickEvent(self, event):
        self.setWindowTitle("Chat")
        self.setMinimumSize(QSize(600, 600))
        self.layout = self.initLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)
        self.show()



