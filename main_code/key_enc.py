import keyring
#import apikey
from cryptography.fernet import Fernet


def enc_key_get(api_key):
    # Step 1: Generate a key using cryptography
    key = Fernet.generate_key()
    print("enc key =  ", key)
    # Step 2: Store that key in Windows Credentials Manager using keyring
    #keyring.set_password('VKR_API_ENC_KEY', 'api_key', key.decode())
    try:
        keyring.set_password('VKR_API_ENC_KEY', 'api_key', key.decode())
    except keyring.errors.KeyringError:
        print('Failed to access the keyring.')
    # Step 3: Encrypt the API key with the generated key
    #api_key = apikey.FirsApiKey()
    api_key = api_key.encode()
    print("api key =  ",api_key)
    cipher = Fernet(key)
    encrypted_api_key = cipher.encrypt(api_key)
    print("api key enc =  ",encrypted_api_key)
    # Step 4: Store the encrypted API key on the file system
    with open('encrypted_api_key.bin', 'wb') as f:
        f.write(encrypted_api_key)