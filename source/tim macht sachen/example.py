# Import the necessary classes
from password_manager import PasswordManager
from user import User

# Step 1: Create a new user with a master password
username = "newName"
master_password = "SuperSecretMaster123!"

# Create a user instance
user = User(username=username, master_password=master_password)
print(user.verify_master_password(username=username, master_password=master_password))
# Step 2: Initialize the Password Manager for this user
password_manager = PasswordManager(user=user)

# Step 3: Add two passwords for this user
password_manager.add_entry(username="github", password="GitHubPassword1!", url="https://github.com", notes="Personal GitHub account")
password_manager.add_entry(username="gmail", password="GmailPassword1!", url="https://mail.google.com", notes="Personal Gmail account")

print("Passwords added successfully!")



# Re-initialize the password manager (simulate logging back in)
user1 = User(username=username, master_password= "SuperSecretMaster123!")
password_manager1 = PasswordManager(user=user1)

# Step 5: Retrieve and print the passwords
github_entry = password_manager1.get_entry("github")
gmail_entry = password_manager1.get_entry("gmail")

print("\nRetrieved Passwords:")
print(f"GitHub: {github_entry}")
print(f"Gmail: {gmail_entry}")
