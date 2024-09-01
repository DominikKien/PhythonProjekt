#pylint: disable=C
import unittest
import sys
sys.path.append('../')
from source.encryption import Encryption  

class TestEncryption(unittest.TestCase):
    def setUp(self) -> None:
        self.masterPassword: str = "testpassword"
        self.encryption: Encryption = Encryption(self.masterPassword)

    def test_derive_key(self) -> None:
        salt: bytes = b'fixed_salt_value'
        key: bytes = self.encryption.deriveKey(self.masterPassword, salt)
        self.assertEqual(len(key), 32) 

    def test_encrypt_decrypt(self) -> None:
        plaintext: str = "This is a secret message"
        encrypted_text: str = self.encryption.encrypt(plaintext)
        decrypted_text: str = self.encryption.decrypt(encrypted_text)

        self.assertEqual(plaintext, decrypted_text)

    def test_encrypt_output_not_plaintext(self) -> None:
        plaintext: str = "Another secret message"
        encrypted_text: str = self.encryption.encrypt(plaintext)

        self.assertNotEqual(plaintext, encrypted_text)
        self.assertIsInstance(encrypted_text, str)

    def test_decrypt_invalid_data(self) -> None:
        with self.assertRaises(ValueError):
            self.encryption.decrypt("invalidciphertext")

    def test_consistent_encryption(self) -> None:
        messages: list[str] = ["Hello World", "123456", "!@#$%^&*()"]
        for message in messages:
            encrypted: str = self.encryption.encrypt(message)
            decrypted: str = self.encryption.decrypt(encrypted)
            self.assertEqual(message, decrypted)

if __name__ == '__main__':
    unittest.main()
