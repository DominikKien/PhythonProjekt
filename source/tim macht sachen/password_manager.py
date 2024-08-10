from encryption import Encryption
from storage import Storage
from user import User

class PasswordManager:
    def __init__(self, user: User, storage_file: str = 'passwords.json'):
        self.user = user
        self.encryption = Encryption(user.master_password_hash)
        self.storage = Storage(storage_file)

    def add_entry(self, username: str, password: str, notes: str = "", category: str = ""):
        encrypted_password = self.encryption.encrypt(password)
        self.storage.add_password(username, encrypted_password, notes, category)

    def get_entry(self, username: str):
        entry = self.storage.get_password(username)
        if entry:
            entry['password'] = self.encryption.decrypt(entry['password'])
        return entry

    def update_entry(self, username: str, new_password: str):
        encrypted_password = self.encryption.encrypt(new_password)
        self.storage.update_password(username, encrypted_password)

    def delete_entry(self, username: str):
        self.storage.delete_password(username)

user = User("bim333", "1234")
pwm = PasswordManager(user)

pwm.add_entry("bim333", "4321", "testing", "test")

