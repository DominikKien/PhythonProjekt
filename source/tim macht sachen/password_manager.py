from encryption import Encryption
from storage import Storage
from user import User

class PasswordManager:
    def __init__(self, user: User, storage_file: str = 'passwords.json'):
        self.user = user
        self.encryption = Encryption(user.master_password_hash)
        self.storage = Storage(storage_file)

    def verify(self) -> bool:
        if len(self.getAllEntryes()) > 0:
            verify = self.get_entry("verify")
            if verify:
                if verify["password"] == "verify":
                    return True
                else:
                    return False
            else:
                self.add_entry("verify", "verify", "", "", "")
                return True
        else: 
            return False
        '''
        verify = self.getAllEntryes()
        print(verify)
        if len(verify) > 0:
            return True
        else:
            print("delete account")
            return False
'''

    
    def add_entry(self, name: str, password: str, url: str, notes: str = "", category: str = ""):
        encrypted_password = self.encryption.encrypt(password)
        self.storage.add_password(username=self.user.username, name=name, password=encrypted_password, url=url, notes=notes, category=category)

    def get_entry(self, name: str):
        entry = self.storage.getEntry(username=self.user.username, name=str(name))
        if entry:
            # Decrypt the password before returning
            entry['password'] = self.encryption.decrypt(entry['password'])
            return entry
        return None

    def update_entry(self, name: str, new_password: str):
        encrypted_password = self.encryption.encrypt(new_password)
        self.storage.update_password(username=self.user.username, name=name, new_password=encrypted_password)

    def delete_entry(self, name: str):
        self.storage.delete_password(username=self.user.username, name=name)
    
    def getAllEntryes(self):
        save = self.storage.getAllEntryes(self.user.username)
        return save
