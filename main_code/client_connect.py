import requests

import socketio
import json
from PyQt6.QtCore import pyqtSignal, QObject
from msg_json import deserialize_history


class ConnectionHandler(QObject):
    receive_msg = pyqtSignal(str)
    chat_history = pyqtSignal(list)
    receive_client_info = pyqtSignal(str)

    def __init__(self, apikey):
        super().__init__()
        self.http_session = requests.Session()
        self.http_session.verify = False
        self.sio = socketio.Client(http_session=self.http_session)
        self.apikey = apikey
        self.chat_ui = None
        self.sio.on("chat_join", self.start_chat)
        self.sio.on("client_info", self.on_client_info)

    def sio_connect(self):
        self.sio.connect('http://46.151.30.76:5000?api_key=' + str(self.apikey))
        self.sio.emit("client_info")

    def sio_disconnect(self):
        self.sio.disconnect()

    def sio_sid(self):
        return self.sio.get_sid()

    def on_chat_msg(self, data):
        self.receive_msg.emit(data)
        print(data)

    def on_history(self, data):
        history = deserialize_history(data)
        array = history.get("messages", "")
        self.chat_history.emit(array)

    def on_client_info(self, data):
        self.receive_client_info.emit(data)

    def start_chat(self, data):
        chat_info = json.loads(data)
        print("chat info     ", chat_info)
        self.sio.on("chat_message", self.on_chat_msg)
        print(json.dumps({"room": chat_info.get('room', ''), "offset": 0}))
        self.chat_ui.chat_info = chat_info
        self.sio.on("chat_history", self.on_history)
        self.sio.emit("chat_history", json.dumps({"room": chat_info.get('room', ''), "offset": 0}))
