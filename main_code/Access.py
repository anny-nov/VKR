import keyring
from cryptography.fernet import Fernet

from FirstAPIKeyDialogWindow import FirstAPIKeyDialogWindow

API_KEY = ''


def get_api_key():
    global API_KEY
    API_KEY = get_dec_key()
    return API_KEY


def get_dec_key():
    try:
        key_str = keyring.get_password('VKR_API_ENC_KEY', 'api_key')
        if key_str is None:
            dlg = FirstAPIKeyDialogWindow()
            dlg.setWindowTitle("First log in")
            dlg.exec()
            return decrypt_key()
        else:
            return decrypt_key()
    except keyring.errors.KeyringError:
        print("error")


def decrypt_key():
    key = keyring.get_password('VKR_API_ENC_KEY', 'api_key').encode()
    with open('encrypted_api_key.bin', "rb") as f:
        cipher_text = f.read()
    cipher_suite = Fernet(key)
    api_key = cipher_suite.decrypt(cipher_text)
    return(api_key.decode())
