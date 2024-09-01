import os
def importFile():
    try:
        #os.remove("passwords.json")
        with open("../importExport/topSecret.json", 'rb') as src:
            with open("passwords.json", 'wb') as dest:
                dest.write(src.read())
    except OSError as e:
        print(f"Error renaming file: {e}")
def exportFile():
    try:
        with open("passwords.json", 'rb') as src:
            with open("../importExport/topSecret.json", 'wb') as dest:
                dest.write(src.read())
        
    except OSError as e:
        print(f"Error renaming file: {e}")
#exportFile()
importFile()