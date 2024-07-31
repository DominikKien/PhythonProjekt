import password as password

class Account(object):

    def __init__(self, email, phoneNumber): # create new account
        self.email = email
        self.phoneNumber = phoneNumber
        self.passwords = []
        pass

    def PassWordWasIsUsed(self):
        pass

    def showUses(self):
        pass

    def export(self):
        pass

    def fImport(self):
        pass

    def loadPassword(self):
        pass

    def addPassword(self, usage, password):
            self.passwords.__add__(password(usage, password))


a1 = Account("tim.brielmayer@gmail.com", 12345678)

a1.addPassword("netflix", 1234)

    