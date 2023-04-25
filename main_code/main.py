from PyQt6.QtWidgets import QApplication
import sys
from MainWindow import MainWindow
from Access import get_api_key
from client_connect import ConnectionHandler
from chat import Dialog

app = QApplication(sys.argv)

window = MainWindow()
window.show()
API_KEY = get_api_key()
#conHand = ConnectionHandler(API_KEY)
#conHand.sio_connect()
#chat_ui = Dialog(conHand)
#conHand.chat_ui = chat_ui
#chat_ui.show()

app.exec()
