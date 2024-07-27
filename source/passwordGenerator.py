import random
import string
import requests
import math
#????????????????
import hashlib



class passwordGenerator():

    url = "https://api.pwnedpasswords.com/range/"


    def __init__(self, length : int, useCapitals : bool =True, useNumbers : bool = True, useSpecialCharacters : bool = True) -> None:
        self.length = length
        self.useCapitals = useCapitals
        self.useNumbers = useNumbers
        self.useSpecialCharacters = useSpecialCharacters
        self.initialSettings()



    def initialSettings(self) -> None:
        self.chars=string.ascii_lowercase
        if self.useCapitals: self.chars += string.ascii_uppercase
        if self.useNumbers: self.chars += string.digits
        if self.useSpecialCharacters: self.chars += "%+'-/!,$"

    def excludeCharacters(self, excludedChars : str) -> None:
        for c in  excludedChars:
            self.chars = self.chars.replace(c, '')

    def haveIBeenPwned(self, password : str) -> bool:
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        result = requests.get(self.url + sha1[:5])
        hashes = (line.split(':') for line in result.text.splitlines())
        for suffix, count in hashes:
            if sha1[5:] == suffix:
                print(f"Password has been breached {count} times.")
                return True
        return False

    def passwordSafety(self, password : str) -> int:
        bruteForceSafety = self.length * math.log2(len(self.chars))
        print(bruteForceSafety)
        if self.haveIBeenPwned(password):
            return 0
        elif bruteForceSafety < 25:
            print("weak")
            return 1
        elif bruteForceSafety >= 25 and bruteForceSafety < 45:
            print("OK")
            return 2
        elif bruteForceSafety >= 45:
            print("strong")
            return 3
        else: return 404

    def generate(self) -> str:
        return ''.join(random.choice(self.chars) for _ in range(self.length))
        
    



pg = passwordGenerator(5, True, True, True)
test = pg.generate()
print(test)
print(pg.passwordSafety(test))