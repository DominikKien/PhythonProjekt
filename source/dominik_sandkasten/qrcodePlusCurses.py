import curses
from twoFactorAuth import TwoFactorAuth

def printqrcode(stdscr: curses.window):
    test = TwoFactorAuth()
    test.generateKey("Meine FResse")
    myList = test.generateQRCode("Meine Fresse")
    
    # Initiale Startposition für das Scrollen
    start_line = 0
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Bestimme, wie viele Zeilen du gleichzeitig anzeigen kannst
        visible_lines = min(height, len(myList))

        # Drucke nur die Zeilen, die in das sichtbare Fenster passen
        if(visible_lines > len(myList)):
            visible_lines = len(myList)
        for i in range(visible_lines):
            yco = i
            row = myList[start_line + i]
            for xco, cell in enumerate(row):
                if cell:
                    stdscr.addstr(yco, xco, "██")
                else:
                    stdscr.addstr(yco, xco, "  ")
        
        stdscr.refresh()

        key = stdscr.getch()

        # Scrolle nach oben, wenn die 'Up'-Taste gedrückt wird
        if key == curses.KEY_UP:
            if start_line > 0:
                start_line -= 1
        
        # Scrolle nach unten, wenn die 'Down'-Taste gedrückt wird
        elif key == curses.KEY_DOWN:
            if start_line < len(myList) - visible_lines:
                start_line += 1
        
        # Beenden, wenn 'q' gedrückt wird
        elif key == ord('q'):
            break
    

def main():
    curses.wrapper(printqrcode)
    

if main():
    main()