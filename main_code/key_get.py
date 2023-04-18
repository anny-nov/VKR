import keyring
from cryptography.fernet import Fernet
import key_enc
from FirstAPIKeyDialogWindow import FirstAPIKeyDialogWindow


def get_dec_key():
    try:
        # Try to get the password from the keyring
        key_str = keyring.get_password('VKR_API_ENC_KEY', 'api_key')
        if key_str is None:
            #key_enc.enc_key_get()
            dlg = FirstAPIKeyDialogWindow()
            dlg.setWindowTitle("First log in")
            dlg.exec()
            return(decrypt_key())
        else:
            return(decrypt_key())
    except keyring.errors.KeyringError:
        print("error")

def decrypt_key():
    key = keyring.get_password('VKR_API_ENC_KEY', 'api_key').encode()
    with open('encrypted_api_key.bin', "rb") as f:
        cipher_text = f.read()
    cipher_suite = Fernet(key)
    api_key = cipher_suite.decrypt(cipher_text)
    #print("done api key  ", api_key)
    return(api_key.decode())
