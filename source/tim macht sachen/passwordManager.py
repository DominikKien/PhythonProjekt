'''Controlls everything with Accountmanagment'''

from datetime import datetime
from encryption import Encryption
from storage import Storage
from user import User

class PasswordManager:
    '''Controller of the Account Managment'''
    def __init__(self, user: User, storageFile: str = 'passwords.json') -> None:
        self.user = user
        self.encryption = Encryption(user.masterPasswordHash)
        self.storage = Storage(storageFile)

    def existingAccountValid(self)-> bool:
        '''checks if existing account is valid'''
        verify = self.getEntry("verify")
        return verify["password"] == "verify"

    def newAccountValid(self) -> bool:
        '''checks if new Account is Valid and creates the verification system'''
        if len(self.getAllEntryes()) == 0:
            self.addEntry("verify", "verify", "", "", "")
            return True
        return False

    def addEntry(self, name: str, password: str, url: str, notes: str = "", category: str = "") -> bool:
        '''adds one entry to the Acount'''
        if name in self.getAllEntryes():
            return False

        encryptedPassword = self.encryption.encrypt(password)
        encryptedDatetime = self.encryption.encrypt(datetime.now().isoformat())
        encryptedUrl = self.encryption.encrypt(url)
        encryptedNotes = self.encryption.encrypt(notes)
        encryptedCategory = self.encryption.encrypt(category)
        self.storage.addPassword(username=self.user.username, name=name, password=encryptedPassword,
                                url=encryptedUrl, notes=encryptedNotes, category=encryptedCategory, datetime = encryptedDatetime)
        return True

    def getEntry(self, name: str) -> dict:
        '''gets the entry with the parameters name'''
        entry = self.storage.getEntry(username=self.user.username, name=str(name))
        if entry:
            entry['password'] = self.encryption.decrypt(entry['password'])
            entry['created_at'] = self.encryption.decrypt(entry['created_at'])
            entry['url'] = self.encryption.decrypt(entry['url'])
            entry['notes'] = self.encryption.decrypt(entry['notes'])
            entry['category'] = self.encryption.decrypt(entry['category'])
            for i in range(len(entry["history"])):
                entry["history"][i] = self.encryption.decrypt(entry["history"][i])
            return entry
        return {}

    def updateEntry(self, name: str, newPassword: str) -> None:
        encryptedPassword = self.encryption.encrypt(newPassword)
        self.storage.updatePassword(username=self.user.username, name=name, newPassword=encryptedPassword)

    def deleteEntry(self, name: str) -> None:
        self.storage.deletePassword(username=self.user.username, name=name)

    def getAllEntryes(self) -> list:
        save = self.storage.getAllEntryes(self.user.username)
        return save

    def getAllEntriesByUrl(self) -> list:
        entryes = self.getAllEntryes()
        entryes = entryes.remove("verify")
        url = {}
        for i in entryes:
            url[self.getEntry(i)["url"]] = i

        sortedUrl = dict(sorted(url.items()))
        return list(sortedUrl.keys())

    def getAllEntriesByName(self) -> list:
        entryes = self.getAllEntryes()
        entryes = entryes.remove("verify")
        return entryes.sort()
        
