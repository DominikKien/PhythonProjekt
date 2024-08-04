#pylint: disable=C
import unittest
import string
import sys
sys.path.append('../')
from source.passwordGenerator import PasswordGenerator

class TestPasswordGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.passGenLower = PasswordGenerator(5, False, False, False)
        self.passGenUpper = PasswordGenerator(5, True, False, False)
        self.passGenNumbers = PasswordGenerator(5, True, True, False)
        self.passGenSC = PasswordGenerator(8)

    def test_init(self) -> None:
        self.assertEqual(self.passGenLower.length, 5)
        self.assertEqual(self.passGenLower.useCapitals, False)
        self.assertEqual(self.passGenLower.useNumbers, False)
        self.assertEqual(self.passGenLower.useSpecialCharacters, False)

    def test_initialSettings(self) -> None:
        self.assertEqual(self.passGenLower.chars, string.ascii_lowercase)
        self.assertEqual(self.passGenUpper.chars, string.ascii_lowercase+string.ascii_uppercase)
        self.assertEqual(self.passGenNumbers.chars, string.ascii_lowercase+string.ascii_uppercase+string.digits)
        self.assertEqual(self.passGenSC.chars, string.ascii_lowercase + string.ascii_uppercase + string.digits + "%+'-/!,$_")
    
    def test_haveIBeenPwned(self) -> None:
        self.assertTrue(self.passGenLower.haveIBeenPwned("1234") > 0)
        self.assertTrue(self.passGenLower.haveIBeenPwned("Xcsiiajsh/&T++*78d.ga,scehw$48e/978rw§tzgfc") == 0)


    def test_excludeCharacters(self) -> None:
        self.passGenLower.excludeCharacters("bcdefghijklmnopqrstuvwxyz")
        self.assertEqual(self.passGenLower.chars, "a")

    def test_generate(self) -> None:
        passLower = self.passGenLower.generate()
        passUpper = self.passGenUpper.generate()
        passNumbers = self.passGenNumbers.generate()
        for u in string.ascii_uppercase:
            self.assertNotIn(u, passLower)
        for n in string.digits:
            self.assertNotIn(n, passLower)
            self.assertNotIn(n, passUpper)
        for sc in "%+'-/!,$":
            self.assertNotIn(sc, passLower)
            self.assertNotIn(sc, passUpper)
            self.assertNotIn(sc, passNumbers)


    def test_containsEverything(self) -> None:
        self.assertTrue(self.passGenLower.containsEverything("abc"))
        self.assertTrue(self.passGenLower.containsEverything("aBc"))
        self.assertTrue(self.passGenLower.containsEverything("aBc123"))
        self.assertTrue(self.passGenLower.containsEverything("aBc123."))
    

    def test_passwordSafety(self) -> None:
        passLower = self.passGenLower.generate()
        passUpper = self.passGenUpper.generate()
        passNumbers = self.passGenNumbers.generate()
        passSC = self.passGenSC.generate()
        breachMessage = f"Password has been breached {self.passGenLower.haveIBeenPwned('12345')} times."
        self.assertEqual(self.passGenLower.passwordSafety("12345"), breachMessage)
        self.assertEqual(self.passGenLower.passwordSafety(passLower), "weak")
        self.assertEqual(self.passGenUpper.passwordSafety(passUpper), "OK")
        self.assertEqual(self.passGenNumbers.passwordSafety(passNumbers), "OK")
        self.assertEqual(self.passGenSC.passwordSafety(passSC), "strong")

    def tearDown(self) -> None:
        del self.passGenLower
        del self.passGenUpper
        del self.passGenNumbers
        del self.passGenSC


if __name__ == "__main__":
    unittest.main()