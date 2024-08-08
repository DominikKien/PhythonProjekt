from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os
import struct


class Account:
    
    
    def __init__(self, master_password: str):
        self.salt = os.urandom(16)
        self.key = derive_key(master_password, self.salt)
        self.passwords = {}

    def add_password(self, service: str, password: str):
        iv, encrypted_password = encrypt_password(password, self.key)
        self.passwords[service] = (iv, encrypted_password)

    def get_password(self, service: str) -> str:
        iv, encrypted_password = self.passwords.get(service)
        if iv and encrypted_password:
            return decrypt_password(iv, encrypted_password, self.key)
        return None

    def save(self, file):
        file.write(self.salt)
        for service, (iv, encrypted_password) in self.passwords.items():
            service_bytes = service.encode('utf-8')
            file.write(struct.pack('I', len(service_bytes)))
            file.write(service_bytes)
            file.write(iv)
            file.write(struct.pack('I', len(encrypted_password)))
            file.write(encrypted_password)

    @staticmethod
    def load(file, master_password: str):
        salt = file.read(16)
        key = derive_key(master_password, salt)
        account = Account.__new__(Account)
        account.salt = salt
        account.key = key
        account.passwords = {}

        while True:
            service_length_data = file.read(4)
            if len(service_length_data) == 0:
                break
            service_length = struct.unpack('I', service_length_data)[0]
            service = file.read(service_length).decode('utf-8')
            iv = file.read(12)
            encrypted_password_length = struct.unpack('I', file.read(4))[0]
            encrypted_password = file.read(encrypted_password_length)
            account.passwords[service] = (iv, encrypted_password)

        return account
    
    

def encrypt_password(password: str, key: bytes) -> (bytes, bytes):
    iv = os.urandom(12)  # 96-bit IV for AES-GCM
    aesgcm = AESGCM(key)
    encrypted_password = aesgcm.encrypt(iv, password.encode(), None)
    return iv, encrypted_password

def decrypt_password(iv: bytes, encrypted_password: bytes, key: bytes) -> str:
    aesgcm = AESGCM(key)
    decrypted_password = aesgcm.decrypt(iv, encrypted_password, None)
    return decrypted_password.decode()

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

class PasswordManager:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account_name: str, master_password: str):
        self.accounts[account_name] = Account(master_password)

    def get_account(self, account_name: str) -> Account:
        return self.accounts.get(account_name)

    def save(self, filename: str):
        with open(filename, 'wb') as file:
            for account_name, account in self.accounts.items():
                account_name_bytes = account_name.encode('utf-8')
                file.write(struct.pack('I', len(account_name_bytes)))
                file.write(account_name_bytes)
                account.save(file)

    def load(self, filename: str):
        with open(filename, 'rb') as file:
            while True:
                account_name_length_data = file.read(4)
                if len(account_name_length_data) == 0:
                    break
                account_name_length = struct.unpack('I', account_name_length_data)[0]
                account_name = file.read(account_name_length).decode('utf-8')
                master_password = input(f"Enter master password for account '{account_name}': ")
                account = Account.load(file, master_password)
                self.accounts[account_name] = account


# Passwortmanager initialisieren
pm = PasswordManager()

# Account hinzufügen
pm.add_account("account1", "master_password1")

# Account bekommen
account = pm.get_account("account1")

# Passwort für einen Dienst hinzufügen
account.add_password("example.com", "my_secure_password")

# Passwort für einen Dienst abrufen
retrieved_password = account.get_password("example.com")
print(f"Retrieved password: {retrieved_password}")

# Passwörter in Datei speichern
pm.save("passwords.dat")

# Passwörter aus Datei laden
pm.load("passwords.dat")
