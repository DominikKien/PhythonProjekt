'''saves username and master password and can hash the password'''

from hashlib import sha256

class User:
    '''defines a user which can be inputed in a Passwordmanager'''
    def __init__(self, username: str, masterPassword: str) -> None:
        self.setUsername(username)
        self.masterPasswordHash = self.hashPassword(masterPassword)

    def hashPassword(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def setUsername(self, username : str) -> None:
        self.username = username
