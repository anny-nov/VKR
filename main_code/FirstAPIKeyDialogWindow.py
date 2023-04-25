import keyring
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
from cryptography.fernet import Fernet



class FirstAPIKeyDialogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        confirmation_buttons = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(confirmation_buttons)
        self.buttonBox.accepted.connect(self.ok_clicked)

        self.layout = QGridLayout()
        message = QLabel("Welcome! Enter your first API Key")
        self.input_box = QLineEdit()
        self.layout.addWidget(message, 0, 0)
        self.layout.addWidget(self.input_box, 1, 0)
        self.layout.addWidget(self.buttonBox, 2, 0)
        self.setLayout(self.layout)

    def ok_clicked(self):
        key = self.input_box.text()
        if len(key) > 0:
            enc_key_get(key)
            self.accept()
        else:
            pass

    def closeEvent(self, event):
        event.ignore()


def enc_key_get(api_key):
    key = Fernet.generate_key()
    try:
        keyring.set_password('VKR_API_ENC_KEY', 'api_key', key.decode())
    except keyring.errors.KeyringError:
        print('Failed to access the keyring.')
    api_key = api_key.encode()
    cipher = Fernet(key)
    encrypted_api_key = cipher.encrypt(api_key)
    with open('encrypted_api_key.bin', 'wb') as f:
        f.write(encrypted_api_key)
