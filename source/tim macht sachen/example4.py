from password_manager import PasswordManager
from user import User

username = "newName"
master_password = "SuperSecretMaster123!"

# Create a user instance
user = User(username=username, master_password=master_password)
password_manager = PasswordManager(user=user)
print(password_manager.newAccountValid())

# Step 3: Add two passwords for this user
password_manager.add_entry(name="github", password="lala!", url="https://github.com", notes="Personal GitHub account")
password_manager.add_entry(name="gmail", password="lulu!", url="https://mail.google.com", notes="Personal Gmail account")

password_manager2 = PasswordManager(user=user)
print(password_manager2.existingAccountValid())
test = password_manager2.getAllEntryes()
test.remove("verify")
for i in test:
    print(password_manager2.get_entry(i))