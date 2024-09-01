import json


class Storage:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.load_data()

    def load_data(self) -> None:
        try:
            with open(self.filepath, 'r') as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    def save_data(self) -> None:
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_password(self, username: str, name: str, password: str, url: str, notes: str, category: str, datetime: str) -> None:
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
        self.save_data()

    def getEntry(self, username: str, name: str) -> dict:
        user_entries = self.data.get(username, [])
        entry = {}
        for entrys in user_entries:
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
        save = []
        user_entries = self.data.get(username, [])
        for entry in user_entries:
            save.append(entry["name"])
        return save

    def update_password(self, username: str, name: str, new_password: str) -> None:
        user_entries = self.data.get(username, [])
        for entry in user_entries:
            if entry["name"] == name:
                entry['history'].append(entry['password'])
                entry['password'] = new_password
                self.save_data()
                return

    def delete_password(self, username: str, name: str) -> None:
        user_entries = self.data.get(username, [])
        self.data[username] = [entry for entry in user_entries if entry["name"] != name]
        self.save_data()
