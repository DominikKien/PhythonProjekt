"""Modul für Ein- und Ausgabe über Terminal"""
import curses
from typing import List, Dict
from user import User
from password_manager import PasswordManager
from passwordGenerator import PasswordGenerator


class Interface:
    """
    Diese Klasse erstellt eine GUI für einen PasswordManager
    """
    def __init__(self) -> None:
        self.layer: int = 0
        self.stdscr: curses.window
        self._lastChooseRow: int = 1
        self.passwordgenerator: PasswordGenerator = PasswordGenerator(6)
        self.entryNumber:int
        self.height:int = -2
        self.offset = 0 # Offset der Pfeile bei Entrys

        self.chooseRow = 1
        self.lengthOfPage = 0
        self.key = ''
        self.currentUser = User(username="", master_password="")
        self.manager = PasswordManager(self.currentUser)

        self.typeMode = False
        self.userName:str = ""
        self.createPassword1:str = ""
        self.createPassword2:str = ""
        self.masterpassword:str = ""

        self.entryName:str = ""
        self.url:str = ""
        self.category:str = ""
        self.note:str = ""

        self.dataList: List[str]

        startPage: List[str] = ["Welcome to Password Manager", "Choose an Account", "Create an Account",  "Close this application"]
        createAccountPage: List[str] = ["Create your Account", "Type your Username", "", "Type your password", "",
                                         "Type your Password again", "", "Create Account", "Generate password"]
        loginAccountPage: List[str] = ["Log into your Account", "Type your Username", "", "Type your password", "", "LogIn"]
        currentAccountPage: List[str] = ["", "Create a new Entry"]
        newEntryPage: List[str] = ["New Entry", "Type your Name for the plattform", "", "Type the url", "", "might assign a category",
                                    "", "Type the password", "", "Might want to add a short Note?", "", "Save","Generate password"]
        showPlattformPage: List[str] = ["Entry", "Name of the plattform", "", "url:", "", "category", "", "password", "", "note", "",
                                         "Save","delete","created at","","last edit", ""]
        self._allPages: List[List[str]] = [startPage, createAccountPage, loginAccountPage, currentAccountPage, newEntryPage, showPlattformPage]

    def showList(self, layer: int) -> int:
        """Gibt die Länge der ausgewählten Liste zurück und zeigt die Ausgewählte Liste im Terminal an"""
        self.offset = 0
        self.layer = layer
        if self.stdscr is None:
            raise ValueError("_stdscr is not initialized.")
        self.stdscr.clear()
        currentPage = self._allPages[layer]
        self.stdscr.addstr(0, 0, currentPage[0])
        for i in range(1, len(currentPage)):
            if i == self.height:
                self.stdscr.addstr(0, 50, "Please extend your terminal in height")
                return i
            self.stdscr.addstr(i, 5, currentPage[i])
        self.stdscr.refresh()
        self._lastChooseRow = 1
        curses.curs_set(0)
        return i + 1

    def showEntry(self, create:bool,height: int) -> int:
        """Zeigt den Eintrag an, falls Create True ist wird das Blanko angezeigt. Bei Create false muss Liste übergeben werden"""
        if create:#Standard DatenListe laden ansonsensten wird übergebene Liste benutzt
            self.dataList = self._allPages[4].copy()
        for i, value in enumerate(self.dataList):
            if i == height:
                self.stdscr.addstr(0, 50, "Please extend your terminal in height")
                return i
            self.stdscr.addstr(i, 40, value)
        return 13 # Save Button

    def extractData(self, data: Dict[str, str]) -> List:
        """Fügt die Daten in der richtigen Liste hinzu"""
        dataList:list
        dataList = self._allPages[5].copy()
        dataList[2] = data["name"]
        self.entryName = data["name"]
        dataList[4] = data["url"]
        self.url = data["url"]
        dataList[6] = data["category"]
        self.category = data["category"]
        dataList[8] = data["password"]
        self.createPassword1 = data["password"]
        dataList[10] = data["notes"]
        self.note = data["notes"]
        dataList[14] = data["created_at"]
        dataList.extend(data["history"])
        return dataList

    def openAccount(self, username: str, password: str) -> PasswordManager:
        currentUser = User(username=username, master_password=password)
        passwordManager = PasswordManager(currentUser)
        return passwordManager

    def handleEnter(self) ->bool:
        """Kümmert sich um die Eingabe der Enter Taste
        return Wert kann bei False andere Handle Taste aufrufen, Multikeyput"""
        self.stdscr.addstr(0, 30, str(self.chooseRow))
        if 5 >= self.layer >= 1 and not self.typeMode:  # Enter ohne Schreibmodus aktiviert
            if self.layer == 1 and self.chooseRow < 7:  # Account Erstelleingabe
                self.stdscr.keypad(False)
                self.typeMode = True
                return True
            if self.layer == 1 and self.chooseRow == 7:  # Account erstellen
                self.stdscr.move(1, 30)
                self.stdscr.clrtoeol()
                if self.createPassword1 != self.createPassword2:  # Verifikation der Daten
                    self.stdscr.addstr(1, 30, "Passwords don't match")
                    return True
                if self.userName == "":
                    self.stdscr.addstr(1, 30, "No Username given")
                    return True
                if not self.passwordgenerator.containsEverything(self.createPassword1):
                    self.stdscr.addstr(1, 30, "Criteria not completed")
                    return True
                self.stdscr.addstr(1, 30, "Account erstellt")
                self.currentUser = User(username=self.userName, master_password=self.createPassword1)  # Account erstellt
                self.manager = PasswordManager(user=self.currentUser)
                self._allPages[3][0] = self.userName
                self.lengthOfPage = self.showList(3)
                return True
            if self.layer == 1 and self.chooseRow == 8:
                self.createPassword1 = self.passwordgenerator.generate()
                self.createPassword2 = self.createPassword1
                self.stdscr.move(4, 4)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(4, 4, self.createPassword2 + "  ")
                self.stdscr.move(6, 4)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(6, 4, self.createPassword2 + "  ")
                return True
            if self.layer == 2 and 0 < self.chooseRow < 5:  # Einloggen Eingabe
                self.stdscr.keypad(False)
                self.typeMode = True
                return True
            if self.layer == 2 and self.chooseRow == 5:  # Account öffnen Login
                self.manager = self.openAccount(username=self.userName, password=self.masterpassword)
                if self.manager.verify():
                    self._allPages[3][0] = self.userName
                    self._allPages[3].extend(self.manager.getAllEntryes())
                    self.lengthOfPage = self.showList(3)
                else:
                    self.stdscr.addstr(1, 30, "Wrong Account Name or Password")
                return True
            if self.layer in(4,5) and 1 <= self.chooseRow <= 10:  # Einloggen Eingabe
                self.stdscr.keypad(False)
                self.typeMode = True
                return True
        if 5 >= self.layer >= 1 and self.typeMode:  # Eingabemodus verlassen
            self.stdscr.keypad(True)
            self.typeMode = False
            return True
        return False


    def handleKeyRight(self)->bool:
        """Kümmert sich um Pfeiltaste Rechts Eingabe"""
        if self.layer == 0:  # Erste Page
            if self.chooseRow == 1:  # Einloggen
                self.lengthOfPage = self.showList(layer=2)
            elif self.chooseRow == 2:  # Account erstellen
                self.lengthOfPage = self.showList(layer=1)
            elif self.chooseRow == 3:  # Schließen Speichern der Daten Hier
                return True
        elif self.layer == 3 and self.lengthOfPage>= self.chooseRow >1: #Einträge anzeigen
            self.entryNumber = self.chooseRow
            self.offset = 36
            self.layer = 5
            self.createPassword1 =""
            self.dataList =self.extractData(self.manager.get_entry(self._allPages[3][self.chooseRow]))
            self.lengthOfPage = self.showEntry(create=False, height= self.height) #Plattform anzeigen
        elif self.layer == 3 and self.chooseRow == 1:#Eintrag erstellen
            self.offset = 36
            self.layer = 4
            self.createPassword1 =""
            self.lengthOfPage = self.showEntry(create=True, height=self.height)
        elif self.layer == 4  and self.chooseRow == 11:#Save new Entry
            if(self.entryName != "" and self.passwordgenerator.containsEverything(self.createPassword1)):
                #self.manager.add_entry(name="github", password="lala!", url="https://github.com/", notes="Personal GitHub account")
                self.manager.add_entry(name = self.entryName, password=self.createPassword1, url= self.url, notes = self.note, category=self.category)
                self._allPages[3].extend(self.manager.getAllEntryes())
                self.lengthOfPage = self.showList(3)
            else:
                self.stdscr.addstr(0, 30, "No name or password does not follow criterias")
        elif self.layer == 5 and self.chooseRow == 11:#Save changend Entry
            if(self.entryName != "" and self.passwordgenerator.containsEverything(self.createPassword1)):
                self.manager = PasswordManager(user = self.currentUser)
                self.manager.update_entry(name = self.entryName, new_password=self.createPassword1)
                self._allPages[3].extend(self.manager.getAllEntryes())
                self.lengthOfPage = self.showList(3)
            else:
                self.stdscr.addstr(0, 30, "No name or password does not follow criterias")
        elif  self.layer == 5 and self.chooseRow == 12:#Delete
            self.manager.delete_entry(self.entryName)
            self._allPages[3].remove(self.entryName)
            self.lengthOfPage = self.showList(3)
        elif self.layer == 4 and self.chooseRow == 12:
            self.createPassword1 = self.passwordgenerator.generate()
            self.stdscr.addstr(8, 40, self.createPassword1 + "  ")
        return False
    def handleKeyLeft(self)->bool:
        """Kümmer sich um Pfeiltaste Links Eingabe"""
        if 3 > self.layer > 0:
            self.userName = ""
            self.lengthOfPage = self.showList(layer=0)  # Eine Seite zurück
        elif self.layer == 3:
            self.lengthOfPage = self.showList(layer=1)  # Eine Seite zurück
            # Hier auch noch Account schließen
        elif 5 <= self.layer >= 4:
            self.lengthOfPage = self.showList(layer=3)  # Eine Seite zurück
            self.offset = 0
        else:
            return True  # Schließen auf der ersten Seite Speichern der Daten Hier
        return False

    def verifyPassword(self)->None:
        """Verifiziert sein Passwort auf Stärke, Benutzer Zeichensatz
            und Wie oft die ersten 5 Hashwerte gepawned wurden
            beim Account erstellen"""
        self.stdscr.addstr(6, 70, "Strength:")
        self.stdscr.move(6, 79)
        self.stdscr.clrtoeol()#Befehl zum restliochen Zeileninhalt löschen
        self.stdscr.addstr(6, 79, self.passwordgenerator.passwordSafety(self.createPassword1))
        self.stdscr.addstr(7, 70, "Criterias:")
        self.stdscr.addstr(7, 81, str(self.passwordgenerator.containsEverything(self.createPassword1)))

    def handleTypemode(self)->None:
        """"Kümmert sich um die Eingabe, Aufruf nur wenn Schreibmodus aktiviert ist"""
        checkPassword = False
        if self.layer == 1:  # Account Erstelleingaben
            checkPassword = self.accountCreation()
        elif self.layer == 2:  # Login Eingabe
            if self.chooseRow in (1, 2):
                if self.key in( '\b','\x7f',curses.KEY_BACKSPACE):
                    self.userName = self.userName[:-1]
                else:
                    self.userName += self.key
                self.stdscr.addstr(2, 4, self.userName + "  ")
            elif self.chooseRow in (3, 4):
                if self.key in('\b','\x7f', curses.KEY_BACKSPACE) :
                    self.masterpassword = self.masterpassword[:-1]
                else:
                    self.masterpassword += self.key
                self.stdscr.addstr(4, 4, self.masterpassword + "  ")
        elif self.layer in(4,5):
            if self.chooseRow in (1, 2):
                if self.key in( '\b','\x7f',curses.KEY_BACKSPACE):
                    self.entryName = self.entryName[:-1]
                else:
                    self.entryName += self.key
                self.stdscr.addstr(2, 40, self.entryName + "  ")
            elif self.chooseRow in (3, 4):
                if self.key in( '\b','\x7f',curses.KEY_BACKSPACE):
                    self.url = self.url[:-1]
                else:
                    self.url += self.key
                self.stdscr.addstr(4, 40, self.url + "  ")
            elif self.chooseRow in (5, 6):
                if self.key in( '\b','\x7f',curses.KEY_BACKSPACE):
                    self.category = self.category[:-1]
                else:
                    self.category += self.key
                self.stdscr.addstr(6, 40, self.category + "  ")
            elif self.chooseRow in (7, 8):
                checkPassword = True
                if self.key in( '\b','\x7f',curses.KEY_BACKSPACE):
                    checkPassword = True
                    self.createPassword1 = self.createPassword1[:-1]
                else:
                    self.createPassword1 += self.key
                self.stdscr.addstr(8, 40, self.createPassword1 + "  ")
            elif self.chooseRow in (9, 10):
                if self.key in( '\b','\x7f',curses.KEY_BACKSPACE):
                    self.note = self.note[:-1]
                else:
                    self.note += self.key
                self.stdscr.addstr(10, 40, self.note + "  ")
        if checkPassword:
            self.verifyPassword()

    def accountCreation(self)->bool:
        """"Eingabe der Accountdaten"""
        checkPassword = False
        if self.chooseRow in (1, 2):  # Username eingabe
            if self.key in ('\b','\x7f',curses.KEY_BACKSPACE):
                self.userName = self.userName[:-1]
            elif len(self.key) == 1 and 32 <= ord(self.key) <= 126:
                self.userName += self.key
            self.stdscr.addstr(2, 4, self.userName + "  ")
        elif self.chooseRow in (3, 4):  # password1
            if self.key in('\b','\x7f',curses.KEY_BACKSPACE):
                self.createPassword1 = self.createPassword1[:-1]
                checkPassword = True
            elif len(self.key) == 1 and 32 <= ord(self.key) <= 126:
                self.createPassword1 += self.key
                checkPassword = True
            self.stdscr.addstr(4, 4, self.createPassword1 + "  ")
        elif self.chooseRow in (5, 6):  # Password 2
            if self.key in('\b','\x7f',curses.KEY_BACKSPACE) :
                self.createPassword2 = self.createPassword2[:-1]
            elif len(self.key) == 1 and 32 <= ord(self.key) <= 126:
                self.createPassword2 += self.key
            self.stdscr.addstr(6, 4, self.createPassword2 + "  ")
        return checkPassword


    def start(self) -> None:
        """Startet das GUI"""
        curses.wrapper(self.main)

    def main(self, stdscr: curses.window) -> None:
        """Wird von start aufgerufen, kümmert sich um die Reaktion auf Tastendrücke"""
        self.stdscr = stdscr
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.clear()
        self.height, _ = self.stdscr.getmaxyx()
        oldheight:int = -2
        while True:
            self.height, _ = self.stdscr.getmaxyx()
            if oldheight != self.height:
                if self.layer < 4:
                    self.lengthOfPage = self.showList(self.layer)
                elif self.layer == 5:
                    self.dataList = self.extractData(self.manager.get_entry(self._allPages[3][self.entryNumber]))
                    self.showEntry(create=False, height = self.height)
                elif self.layer == 4:
                    self.showEntry(create=True, height = self.height)
            oldheight = self.height
            #self.chooseRow = self._lastChooseRow
            if self.chooseRow is None:
                self.chooseRow = 1
            self.key = self.stdscr.getkey()
            # self._stdscr.addstr(6, 0, key)
            if self.key in ('\n', '\r', curses.KEY_ENTER):  # Enter
                if not self.handleEnter():
                    self.handleKeyRight()
            elif self.key == "KEY_UP":  # Up
                self.chooseRow -= 1
            elif self.key == "KEY_DOWN":  # Down
                self.chooseRow += 1
            elif self.key == "KEY_LEFT":    # Left
                if self.handleKeyLeft():
                    break
            elif self.key == "KEY_RIGHT":  # Right
                if self.handleKeyRight():
                    break

            # Der Ganze Rest der Tastatur dadrunter
            elif self.typeMode:
                self.handleTypemode()

            if self.chooseRow > self.lengthOfPage - 1:
                self.chooseRow = 1
            elif self.chooseRow < 1:
                self.chooseRow = self.lengthOfPage - 1

            self.stdscr.addstr(self._lastChooseRow, self.offset, "    ")
            self.stdscr.addstr(self.chooseRow, self.offset, "--->")
           #self.stdscr.addstr(5, 0, str(self.layer))
            curses.curs_set(0)
            self._lastChooseRow = self.chooseRow
            self.stdscr.refresh()

        curses.nocbreak()
        #stdscr.keypad(False)
        curses.echo()


def main() -> None:
    interface = Interface()
    interface.start()


main()
