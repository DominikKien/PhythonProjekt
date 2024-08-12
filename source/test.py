import string

char = 'g'

if char in string.ascii_uppercase:
    print(f"'{char}' ist ein Großbuchstabe.")
else:
    print(f"'{char}' ist kein Großbuchstabe.")