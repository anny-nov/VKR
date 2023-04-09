from main_code.FirstAPIKeyDialogWindow import FirstAPIKeyDialogWindow

API_KEY = ''

def check_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    if len(key) == 0:
        dlg = FirstAPIKeyDialogWindow()
        dlg.setWindowTitle("First log in")
        dlg.exec()
    fill_api_key()

def fill_api_key():
    key_file = open('../api_key', 'r+')
    key = str(key_file.read())
    global API_KEY
    API_KEY = key

def get_api_key():
    global API_KEY
    check_api_key()
    return API_KEY