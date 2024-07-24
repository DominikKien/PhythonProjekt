import random
import string



class passwordGenerator():
    def passwordGenerator(self) -> None:
        pass



    def generateStarter(self) -> str:
        chars=string.ascii_letters + string.digits + string.punctuation
        print(chars)
        return ''.join(random.choice(chars) for _ in range(random.randint(8, 20)))
    



pg = passwordGenerator()
print(pg.generateStarter())