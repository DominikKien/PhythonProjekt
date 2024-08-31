from password_manager import PasswordManager
from user import User

username2 = "newName2"
master_password2 = "SuperSecretMaster123!2"

user3 = User(username=username2, master_password=master_password2)
password_manager3 = PasswordManager(user=user3)

test = password_manager3.getAllEntryes()

#for i in test:
#    entry = password_manager3.get_entry(i)
#    print(entry)

username = "newName2"
password = "SuperSecretMaster1!2"

user = User(username=username, master_password=password)
password_manager = PasswordManager(user=user)



print(password_manager3.verify())

print(password_manager.verify())