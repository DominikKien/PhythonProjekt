from password_manager import PasswordManager
from user import User

username = "hey"
password = "1234"

u = User(username=username, master_password=password)
m = PasswordManager(u)

m.add_entry(name="github", password="lala!", url="https://github.com", notes="Personal GitHub account")

#print(m.getAllEntryes())
#print(m.get_entry("github"))
#m.update_entry("github", "hehe")

print(m.get_entry("github"))

#m.delete_entry("github")