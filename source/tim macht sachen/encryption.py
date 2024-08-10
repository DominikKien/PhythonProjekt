from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

class Encryption:
    def __init__(self, master_password: str):
        self.backend = default_backend()
        self.salt = os.urandom(16)
        self.key = self.derive_key(master_password)

    def derive_key(self, master_password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        return urlsafe_b64encode(kdf.derive(master_password.encode()))

    def encrypt(self, plaintext: str) -> str:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return urlsafe_b64encode(iv + ciphertext).decode('utf-8')

    def decrypt(self, ciphertext: str) -> str:
        data = urlsafe_b64decode(ciphertext.encode('utf-8'))
        iv = data[:16]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(data[16:]) + decryptor.finalize()
        return plaintext.decode('utf-8')
