from password_manager import PasswordManager
from user import User

# Step 1: Create a new user with a master password
username = "newName"
master_password = "SuperSecretMaster123!"

# Create a user instance
user = User(username=username, master_password=master_password)
print(user.verify_master_password("SuperSecretMaster123!"))
# Step 2: Initialize the Password Manager for this user
password_manager = PasswordManager(user=user)

username2 = "newName2"
master_password2 = "SuperSecretMaster123!2"


user2 = User(username=username2, master_password=master_password2)

# Step 2: Initialize the Password Manager for this user
password_manager2 = PasswordManager(user=user2)

# Step 3: Add two passwords for this user
password_manager.add_entry(username="github", password="GitHubPassword1!", url="https://github.com", notes="Personal GitHub account")
password_manager.add_entry(username="gmail", password="GmailPassword1!", url="https://mail.google.com", notes="Personal Gmail account")

print("Passwords added successfully!")


user3 = User(username=username2, master_password=master_password2)
password_manager3 = PasswordManager(user=user3)

github_entry = password_manager3.get_entry("github")
gmail_entry = password_manager3.get_entry("gmail")

print("\nRetrieved Passwords:")
print(f"GitHub: {github_entry}")
print(f"Gmail: {gmail_entry}")

user4 = User(username=username, master_password=master_password)
password_manager4 = PasswordManager(user=user4)

github_entry = password_manager4.get_entry("github")
gmail_entry = password_manager4.get_entry("gmail")

print("\nRetrieved Passwords:")
print(f"GitHub: {github_entry}")
print(f"Gmail: {gmail_entry}")