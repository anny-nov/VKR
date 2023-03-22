import os

import requests

from main_code.APIKeyDialogWindow import APIKeyDialogWindow
from main_code.QRCodeDialog import QRCodeDialog

API_KEY = ''

def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key

def new_APIKey(self):
    dlg = APIKeyDialogWindow(self)
    dlg.setWindowTitle("New API Key Creation")
    if dlg.exec():
        dlg_qr = QRCodeDialog(self)
        dlg_qr.setWindowTitle("QRCode")
        if dlg_qr.exec():
            os.remove('api_key_qr.png')

def DeactivateComputer(self):
    pass

def DeleteComputer(self, hardware_id):
    api_url = 'http://46.151.30.76:5000/api/computer?hardware_id=' + hardware_id + '&api_key=' + API_KEY
    requests.delete(api_url, params=hardware_id)
    self.close()