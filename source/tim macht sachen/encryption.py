from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

class Encryption:
    def __init__(self, master_password: str):
        self.backend = default_backend()
        self.master_password = master_password

    def derive_key(self, master_password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes = 256 bits for AES-256
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(master_password.encode('latin-1'))

    def encrypt(self, plaintext: str) -> str:
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self.derive_key(self.master_password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode('latin-1')) + encryptor.finalize()
        encrypted_data = urlsafe_b64encode(salt + iv + ciphertext).decode('latin-1')
        return encrypted_data

    def decrypt(self, ciphertext: str) -> str:
        data = urlsafe_b64decode(ciphertext.encode('latin-1'))
        salt = data[:16]  # Extract the salt
        iv = data[16:32]  # Extract the IV
        ciphertext = data[32:]  # Extract the ciphertext
        key = self.derive_key(self.master_password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode('latin-1')
