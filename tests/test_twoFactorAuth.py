#pylint: disable=C
import sys
import pyotp
import unittest
sys.path.append('../')
from source.twoFactorAuth import TwoFactorAuth

class TestTwoFactorAuth(unittest.TestCase):
    def setUp(self) -> None:
        self.tfa = TwoFactorAuth()

    def test_generateKey(self) -> None:
        self.assertIsNot(self.tfa.generateKey, "")

    def test_verifyCode(self) -> None:
        key = self.tfa.generateKey("Unittest")
        totp = pyotp.TOTP(key)
        self.assertTrue(self.tfa.verifyCode(totp.now()))
    
    def tearDown(self) -> None:
        del self.tfa
    
if __name__ == "__main__":
    unittest.main()