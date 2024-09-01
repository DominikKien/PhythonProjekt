from encryption import Encryption
from storage import Storage
from datetime import datetime
from user import User

class PasswordManager:
    def __init__(self, user: User, storage_file: str = 'passwords.json') -> None:
        self.user = user
        self.encryption = Encryption(user.master_password_hash)
        self.storage = Storage(storage_file)

    def existingAccountValid(self)-> bool:
        verify = self.get_entry("verify")
        if verify["password"] == "verify":
            return True
        else:
            return False
    
    def newAccountValid(self) -> bool: 
        if len(self.getAllEntryes()) > 0:
            return False
        else: 
            self.add_entry("verify", "verify", "", "", "")
            return True
         
        '''
        verify = self.getAllEntryes()
        print(verify)
        if len(verify) > 0:
            return True
        else:
            print("delete account")
            return False
'''

    
    def add_entry(self, name: str, password: str, url: str, notes: str = "", category: str = "") -> bool:
        if (name in self.getAllEntryes()):
            return False
        else:
            encrypted_password = self.encryption.encrypt(password)
            encrypted_datetime = self.encryption.encrypt(datetime.now().isoformat())
            encrypted_url = self.encryption.encrypt(url)
            encrypted_notes = self.encryption.encrypt(notes)
            encrypted_category = self.encryption.encrypt(category)
            self.storage.add_password(username=self.user.username, name=name, password=encrypted_password, url=encrypted_url, notes=encrypted_notes, category=encrypted_category, datetime = encrypted_datetime)
            #self.verify()
            return True

    def get_entry(self, name: str) -> dict:
        entry = self.storage.getEntry(username=self.user.username, name=str(name))
        if entry:
            # Decrypt the password before returning
            entry['password'] = self.encryption.decrypt(entry['password'])
            entry['created_at'] = self.encryption.decrypt(entry['created_at'])
            entry['url'] = self.encryption.decrypt(entry['url'])
            entry['notes'] = self.encryption.decrypt(entry['notes'])
            entry['category'] = self.encryption.decrypt(entry['category'])
            for i in range(len(entry["history"])):
                entry["history"][i] = self.encryption.decrypt(entry["history"][i]) 
            return entry
        return {}

    def update_entry(self, name: str, new_password: str) -> None:
        encrypted_password = self.encryption.encrypt(new_password)
        self.storage.update_password(username=self.user.username, name=name, new_password=encrypted_password)

    def delete_entry(self, name: str) -> None:
        self.storage.delete_password(username=self.user.username, name=name)
    
    def getAllEntryes(self) -> list:
        save = self.storage.getAllEntryes(self.user.username)
        return save
