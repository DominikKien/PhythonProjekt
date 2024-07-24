import curses
accounts = ["Tim", "Justin", "Dominik"]

data = [
    {
        "category": "category1",
        "plattform": "Netflix",
        "password": "HAHAHA1234_Ü",
        "note 1": "Das Password ist falsch"
    },

    {
        "category": "category1",
        "plattform": "LeagueOfLegends",
        "password": "Kinderpasswort!!_.ÄÖ",
        "note 1": "Das Password ist falsch"
    }
]

class Interface:
    def __init__ (self, accounts:list ):
        print("I have been initiliased")
        self._accounts = accounts

    def showRespone(self):
        print("Im Alive")

    def getdata(self, data:list):
        self._data = data

    def getMasterPassword(self):
        print("Master Password Eingabe\n")
        return  input() #Initialiesieren der Account Funktion über main
    
    def start(self):
        print("hier2")
        def main(stdscr):
            # Kein Echo der Tastendrücke
            curses.noecho()
            # Sofortige Reaktion auf Tastendrücke (keine Zeilenpufferung)
            curses.cbreak()
            # Spezielle Tasten wie Pfeiltasten aktivieren
            stdscr.keypad(True)

            stdscr.addstr(0, 0, "Drücke eine Pfeiltaste (oben, unten, links, rechts) oder 'q' zum Beenden.")

            while True:
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    stdscr.addstr(1, 0, "Pfeiltaste oben gedrückt.   ")
                elif key == curses.KEY_DOWN:
                    stdscr.addstr(1, 0, "Pfeiltaste unten gedrückt.  ")
                elif key == curses.KEY_LEFT:
                    stdscr.addstr(1, 0, "Pfeiltaste links gedrückt.  ")
                elif key == curses.KEY_RIGHT:
                    stdscr.addstr(1, 0, "Pfeiltaste rechts gedrückt. ")
                elif key == ord('q'):
                    break
                
                stdscr.refresh()

            # Rückkehr zu den Standardeinstellungen
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
        curses.wrapper(main)
    
    
        
    

def main():
    
    test: Interface = Interface(accounts= accounts)
    test.showRespone()
    test.start()
main()

    