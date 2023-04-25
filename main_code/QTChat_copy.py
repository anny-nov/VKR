import datetime

import socketio
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget, QMainWindow, QVBoxLayout, QListWidget, \
    QListWidgetItem, QPushButton

from PyQt6 import QtWidgets

from Access import get_api_key
from chat import Dialog
from client_connect import ConnectionHandler

API_KEY = ''


class Chat_Widget(QMainWindow):
    def __init__(self):
        super().__init__()

    def initLayout(self):
        chat_layout = QGridLayout()
        chat_layout.setSpacing(10)

        self.message_history_widget=QWidget(self)
        self.message_history_widget.setStyleSheet("background-color:white;")
        self.message_history_widget.setMinimumSize(100, 200)
        layout = QVBoxLayout()
        self.message_history_widget.setLayout(layout)
        self.message_history = QListWidget(self.message_history_widget)
        self.message_history.setWordWrap(True)
        self.message_history_widget.layout().addWidget(self.message_history)

        self.lineEdit = QtWidgets.QLineEdit(self)

        self.chat_button = QPushButton(self)
        self.chat_button.setText("Open Chat")
        self.chat_button.clicked.connect(lambda: self.open_chat())
        print('button is creating')

        chat_layout.setColumnStretch(0, 10)
        chat_layout.addWidget(self.message_history_widget, 0, 0, 1, 2)
        chat_layout.addWidget(self.chat_button, 1, 0, 1, 1)
        chat_layout.setVerticalSpacing(4)
        return chat_layout

    def open_chat(self):
        global API_KEY
        API_KEY = get_api_key()
        self.conHand = ConnectionHandler(API_KEY)
        self.conHand.sio_connect()
        self.chat_ui = Dialog(self.conHand)
        self.conHand.chat_ui = self.chat_ui
        self.chat_ui.show()



