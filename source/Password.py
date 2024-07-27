import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import bcrypt
class Password :

    def __init__(self, usage, password): #To create new password
        self.usage = usage
        self.password = password

    def __init__(self):#To read existing password
        pass

    def derive_key(password, salt):
        return bcrypt.kdf(password=password.encode(), salt=salt, desired_key_bytes=32, rounds=100)

    def encode(plaintext,  password):
        salt = get_random_bytes(16)  # Generate a random salt
        key = derive_key(password, salt)  # Derive the key using the salt
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = pad(plaintext.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        return base64.b64encode(salt + iv + ciphertext).decode('utf-8')

    def decode(ciphertext,  password):
        decoded = base64.b64decode(ciphertext)
        salt = decoded[:16]  # Extract the salt
        iv = decoded[16:32]  # Extract the IV
        actual_ciphertext = decoded[32:]
        key = derive_key(password, salt)  # Derive the key using the salt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(actual_ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        return plaintext.decode('utf-8')
    
    

    def writePassword(passwords, filename, password):
        encrypted_passwords = {k: encode(v, password) for k, v in passwords.items()}
        with open(filename, 'w') as file:
            json.dump(encrypted_passwords, file)

    def loadPasswords(filename, password):
        if not os.path.exists(filename):
            return {}
        with open(filename, 'r') as file:
            encrypted_passwords = json.load(file)
        return {k: decode(v, password) for k, v in encrypted_passwords.items()}

        