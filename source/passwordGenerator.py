"""Module for generating passwords"""
import random
import string
import math
import hashlib
import requests



def haveIBeenPwned(password : str) -> int:

    """Checks, wether a password has been breached before and how many times it has been breached"""

    url = "https://api.pwnedpasswords.com/range/"
    breachCount = 0
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    result = requests.get(url + sha1[:5])
    if result.status_code != 200:
        print("Warning: Cannot check if password has been breached. Please check your internet connection.")
        return 0
    hashes = (line.split(':') for line in result.text.splitlines())
    for suffix, count in hashes:
        if sha1[5:] == suffix:
            breachCount = int(count)
    return int(breachCount)


class PasswordGenerator():

    """
    This class generates a password based on different criteria and checks its strength and wether it's been pwned.
    """


    def __init__(self, length : int, useCapitals : bool =True, useNumbers : bool = True, useSpecialCharacters : bool = True) -> None:
        self.length = length
        self.useCapitals = useCapitals
        self.useNumbers = useNumbers
        self.useSpecialCharacters = useSpecialCharacters
        self.chars = string.ascii_lowercase
        self.initialSettings()

    def initialSettings(self) -> None:

        """Defines set of characters this class will use"""

        if self.useCapitals:
            self.chars += string.ascii_uppercase
        if self.useNumbers:
            self.chars += string.digits
        if self.useSpecialCharacters:
            self.chars += "%+'-/!,$_"

    def excludeCharacters(self, excludedChars : str) -> None:

        """Excludes specific characters"""

        for char in  excludedChars:
            self.chars = self.chars.replace(char, '')


    def passwordSafety(self, password : str) -> str:

        """Calculates the safety of a password"""

        bruteForceSafety = int(self.length * math.log2(len(self.chars)))
        #Pwned password
        if haveIBeenPwned(password) > 0:
            return f"Password has been breached {haveIBeenPwned(password)} times."
        #Weak password
        if bruteForceSafety < 25:
            return "weak"
        #OK password
        if 25 <= bruteForceSafety < 45:
            return "OK"
        #strong password
        if bruteForceSafety >= 45:
            return "strong"
        return  "Something went wrong"




    def containsEverything(self, testPW : str) -> bool:

        """Checks if the password contains at least one of the requested characters"""
        if self.useCapitals:
            contains1 = False
        else:
            contains1 = True
        if self.useNumbers:
            contains2 = False
        else:
            contains2 = True
        if self.useSpecialCharacters:
            contains3 = False
        else:
            contains3 = True

        for char in testPW:
            if char in string.ascii_uppercase:
                contains1 = True
            if char in string.digits:
                contains2 = True
            if char in "%+'-/!,$_":
                contains3 = True
        return contains1 and contains2 and contains3

    def generate(self) -> str:

        """Generates a random password with given criterias"""

        passwordAttempt = ""
        while not self.containsEverything(passwordAttempt):
            passwordAttempt = ''.join(random.choice(self.chars) for _ in range(self.length))
        return passwordAttempt
