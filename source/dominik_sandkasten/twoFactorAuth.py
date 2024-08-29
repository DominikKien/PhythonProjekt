"""This module handles the two factor authentication"""

import pyotp
import qrcode #type: ignore

class TwoFactorAuth():

    """Class handling the two factor authentication"""

    def __init__(self, key : str = "") -> None:
        self.key = key
        self.totp = pyotp.TOTP(self.key)

    def generateKey(self, accountName : str) -> str:

        """Generates the key, only executed once per account"""

        self.key = pyotp.random_base32()
        return self.key

    def generateQRCode(self, accountName : str) -> list:

        """Generates the QR-Code, only executed once per account"""

        uri = pyotp.totp.TOTP(self.key).provisioning_uri(name = accountName, issuer_name = "Password Manager")
        qrCode = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qrCode.add_data(uri)
        qrCode.make(fit=True)
        return qrCode.get_matrix()

    def verifyCode(self, enteredCode : str) -> bool:

        """Verifying the entered one time password"""

        totp = pyotp.TOTP(self.key)
        if enteredCode == totp.now():
            return True
        return False
