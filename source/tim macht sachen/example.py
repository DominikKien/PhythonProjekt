from password_manager import PasswordManager
from user import User

# Step 1: Create a new user with a master password
username = "newName"
master_password = "SuperSecretMaster123!"

# Create a user instance
user = User(username=username, master_password=master_password)
print(user.verify_master_password("SuperSecretMaster123!"))


username2 = "newName2"
master_password2 = "SuperSecretMaster123!2"


user2 = User(username=username2, master_password=master_password2)

#password_manager2.getAllEntryes()
# Step 3: Add two passwords for this user
#password_manager.add_entry(name="github", password="lala!", url="https://github.com", notes="Personal GitHub account")
#password_manager.add_entry(name="gmail", password="lulu!", url="https://mail.google.com", notes="Personal Gmail account")

#password_manager2.add_entry(name="github", password="GitHubPassword1!", url="https://github.com", notes="Personal GitHub account")
#password_manager2.add_entry(name="gmail", password="GmailPassword1!", url="https://mail.google.com", notes="Personal Gmail account")

print("Passwords added successfully!")


user3 = User(username=username2, master_password=master_password2)
password_manager3 = PasswordManager(user=user3)

user4 = User(username=username, master_password=master_password)
password_manager4 = PasswordManager(user=user4)

github_entry = password_manager4.get_entry("github")
gmail_entry = password_manager4.get_entry("gmail")

print("\nRetrieved Passwords:")
print(f"GitHub: {github_entry}")
print(f"Gmail: {gmail_entry}")

print(password_manager4.getAllEntryes())

print("HIER")
test = password_manager3.getAllEntryes()
print(test[0])
print(test[1])

for i in test:
    entry = password_manager3.get_entry(i)
    print(entry)

'''
github_entry = password_manager3.get_entry(test[0])
gmail_entry = password_manager3.get_entry(test[1])

print("\nRetrieved Passwords:")
print(f"GitHub: {github_entry}")
print(f"Gmail: {gmail_entry}")

'''


'''
github_entry = password_manager3.get_entry("github")
gmail_entry = password_manager3.get_entry("gmail")

print("\nRetrieved Passwords:")
print(f"GitHub: {github_entry}")
print(f"Gmail: {gmail_entry}")
'''