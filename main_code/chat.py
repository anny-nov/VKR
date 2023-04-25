import json
from PyQt6.QtWidgets import QDialog, QListWidgetItem

from ui_chat import Ui_Dialog as dialog
from recieveWidget import Widget as recW
from sendWidget import Widget as senW
from msg_json import serialize_message, deserialize_client_info
from msg_json import deserialize_message


class Dialog(QDialog, dialog):

    def __init__(self, con):
        super(Dialog, self).__init__()
        QDialog.__init__(self)
        self.con = con
        self.chat_info = None
        self.sio = self.con.sio
        self.offset = 0
        self.my_client_info = None

        self.setupUi(self)
        self.sendbtn.clicked.connect(lambda: self.send_message(self.mlineEdit.text()))
        self.scroll_bar = self.ChatlistWidget.verticalScrollBar()
        self.scroll_bar.valueChanged.connect(self.onScroll)

        self.con.receive_msg.connect(self.receive_message)
        self.con.chat_history.connect(self.append_history)
        self.con.receive_client_info.connect(self.receive_client_info)

    def onScroll(self, rowPosition):
        if self.scroll_bar.minimum() == rowPosition:
            history_info = json.dumps({"room": self.chat_info.get('room', ''), "offset": self.offset})
            self.sio.emit("chat_history", history_info)

    def receive_client_info(self, data):
        client_info = deserialize_client_info(data)
        self.my_client_info = client_info

    def show_msg(self, message, sender, insert_pos=None):
        sender.message.setText(message.get('msg', ''))
        sender.label.setText(message.get("from_name", "unknown"))
        item = QListWidgetItem()
        item.setSizeHint(sender.sizeHint())
        if insert_pos == None:
            self.ChatlistWidget.addItem(item)
            self.ChatlistWidget.setItemWidget(item, sender)
            self.ChatlistWidget.setMinimumWidth(sender.width())
            self.ChatlistWidget.scrollToBottom()
        else:
            self.ChatlistWidget.insertItem(insert_pos, item)
            self.ChatlistWidget.setItemWidget(item, sender)
            self.ChatlistWidget.setMinimumWidth(sender.width())

    def send_message(self, message_text):
        sendW = senW()
        _from = self.my_client_info.get("id", '')
        name = self.my_client_info.get("name", '')
        room = self.chat_info.get('room', '')
        if message_text:
            message = serialize_message(_from, room, message_text, name)
            self.sio.emit('chat_message', json.dumps(message))
            self.show_msg(message, sendW)

    def receive_message(self, data):
        message = deserialize_message(data)
        reciW = recW()
        self.show_msg(message, reciW)

    def append_history(self, data):
        print(self.offset)
        _from = 2
        insert_pos = None
        last_message = None
        if self.offset != 0:
            insert_pos = 0
            last_message = self.ChatlistWidget.item(0)
            data.reverse()

        for item in data:
            sender = item.get('from', '')
            if sender == _from:
                sendW = senW()
                self.show_msg(item, sendW, insert_pos)

            else:
                reciW = recW()
                self.show_msg(item, reciW, insert_pos)

            if insert_pos == 0:
                self.ChatlistWidget.scrollToItem(last_message)

        if self.offset == 0:
            self.ChatlistWidget.scrollToBottom()

        self.offset += 1

    def closeEvent(self, event):
        self.con.sio_disconnect()
