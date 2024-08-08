import pyotp
import qrcode

class TwoFactorAuth():
    def __init__(self) -> None:
        self.key = ""
        self.totp = pyotp.TOTP(self.key)

    def generateKey(self, accountName : str) -> None:
        self.key = pyotp.random_base32()
        self.generateQRCode(accountName)

    def generateQRCode(self, accountName : str) -> None:
        uri = pyotp.totp.TOTP(self.key).provisioning_uri(name = accountName, issuer_name = "Password Manager")
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        qr_terminal = qr.print_ascii(invert=True)

    def verifyCode(self, enteredCode : str) -> bool:
        totp = pyotp.TOTP(self.key)
        if enteredCode == totp.now():
            print("Richtig!!")
            return True
        print("Falsch!!")
        return False

    
ta = TwoFactorAuth()
ta.generateKey("JustinTest")
while True:
    enteredCode = input("Please enter one-time password: ")
    ta.verifyCode(enteredCode)