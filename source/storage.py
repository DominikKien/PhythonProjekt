''' This is for storage managment'''

import json

class Storage:
    '''reads from File and writes in File'''
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.loadData()

    def loadData(self) -> None:
        '''loads the Current json file'''
        try:
            with open(self.filepath, 'r', encoding="utf-8") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    def saveData(self) -> None:
        with open(self.filepath, 'w', encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def addPassword(self, username: str, name: str, password: str, url: str, notes: str, category: str, datetime: str) -> None:
        ''' adds the given data to json'''
        entry = {
            "name": name,
            "password": password,
            "url": url,
            "notes": notes,
            "category": category,
            "created_at": datetime,
            "history": []
        }
        if username not in self.data:
            self.data[username] = []
        self.data[username].append(entry)
        self.saveData()

    def getEntry(self, username: str, name: str) -> dict:
        ''' gets one entry by the parameter name of the password'''
        userEntries = self.data.get(username, [])
        entry = {}
        for entrys in userEntries:
            if entrys["name"] == name:
                entry["name"] = entrys["name"]
                entry["password"] = entrys["password"]
                entry["url"] = entrys["url"]
                entry["notes"] = entrys["notes"]
                entry["category"] = entrys["category"]
                entry["created_at"] = entrys["created_at"]
                entry["history"] = entrys["history"]
                return entry
        return entry

    def getAllEntryes(self, username:str) -> list:
        '''gives back all Entryes of selected user'''
        save = []
        userEntries = self.data.get(username, [])
        for entry in userEntries:
            save.append(entry["name"])
        return save

    def updatePassword(self, username: str, name: str, newPassword: str) -> None:
        '''saves the updated password in the file'''
        userEntries = self.data.get(username, [])
        for entry in userEntries:
            if entry["name"] == name:
                entry['history'].append(entry['password'])
                entry['password'] = newPassword
                self.saveData()
                return

    def deletePassword(self, username: str, name: str) -> None:
        userEntries = self.data.get(username, [])
        self.data[username] = [entry for entry in userEntries if entry["name"] != name]
        self.saveData()
