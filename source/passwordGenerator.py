"""Module for generating passwords"""

import random
import string
import math
import hashlib
import requests



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

    def haveIBeenPwned(self, password : str) -> int:

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
                breachCount = count
        return int(breachCount)

    def passwordSafety(self, password : str) -> str:

        """Calculates the safety of a password"""

        bruteForceSafety = self.length * math.log2(len(self.chars))
        message = ""
        #Pwned password
        if self.haveIBeenPwned(password) > 0:
            message = f"Password has been breached {self.haveIBeenPwned(password)} times."
        #Weak password
        elif bruteForceSafety < 25:
            message = "weak"
        #OK password
        elif 25 <= bruteForceSafety < 45:
            message = "OK"
        #strong password
        elif bruteForceSafety >= 45:
            message = "strong"
        message =  "Something went wrong"
        return message

    def containsEverything(self, testPW : str) -> bool:

        """Checks if the password contains at least one of the requested characters"""

        contains = True
        if string.ascii_uppercase in testPW != self.useCapitals:
            contains = False
        if string.digits in testPW != self.useNumbers:
            contains = False
        if "%+'-/!,$_" in testPW != self.useCapitals:
            contains = False
        return contains

    def generate(self) -> str:

        """Generates the password"""

        passwordAttempt = ""
        while not self.containsEverything(passwordAttempt):
            passwordAttempt = ''.join(random.choice(self.chars) for _ in range(self.length))
        return passwordAttempt
