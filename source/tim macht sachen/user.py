from hashlib import sha256

class User:
    def __init__(self, username: str, master_password: str):
        self.username = username
        self.master_password_hash = self.hash_password(master_password)

    def hash_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def verify_master_password(self, master_password: str) -> bool:
        return self.master_password_hash == self.hash_password(master_password)
