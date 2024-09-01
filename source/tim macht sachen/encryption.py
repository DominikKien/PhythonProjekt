'''encrypts and decrypts everything'''

from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class Encryption:
    '''Function encrypt -> encrypts Data
    Function decrypt -> decrits Data'''
    def __init__(self, masterPassword: str):
        self.backend = default_backend()
        self.masterPassword = masterPassword

    def deriveKey(self, masterPassword: str, salt: bytes) -> bytes:
        '''delivers the key to encrypt and decrypt'''
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes = 256 bits for AES-256
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(masterPassword.encode('latin-1'))

    def encrypt(self, plaintext: str) -> str:
        '''encryptes whats given as a parameter and the encrypted version gets retrned'''
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self.deriveKey(self.masterPassword, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode('latin-1')) + encryptor.finalize()
        encryptedData = urlsafe_b64encode(salt + iv + ciphertext).decode('latin-1')
        return encryptedData

    def decrypt(self, ciphertext: str) -> str:
        '''decryptes whats given as a parameter and the decrypted version gets retrned'''
        data = urlsafe_b64decode(ciphertext.encode('latin-1'))
        salt = data[:16]  # Extract the salt
        iv = data[16:32]  # Extract the IV

        myBytes = data[32:]  # Extract the ciphertext
        key = self.deriveKey(self.masterPassword, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(myBytes) + decryptor.finalize()
        return plaintext.decode('latin-1')
