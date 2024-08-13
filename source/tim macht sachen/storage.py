import json
from datetime import datetime
from typing import Dict, List
class Storage:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self) -> Dict:
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_password(self, username: str, name: str, password: str, url: str, notes: str = "", category: str = ""):
        entry = {
            "name": name,
            "password": password,
            "url": url,
            "notes": notes,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "history": []
        }
        if username not in self.data:
            self.data[username] = []
        self.data[username].append(entry)
        self.save_data()

    def get_password(self, username: str, name: str) -> Dict:
        user_entries = self.data.get(username, [])
        for entry in user_entries:
            if entry["name"] == name:
                return entry
        return None

    def update_password(self, username: str, name: str, new_password: str):
        user_entries = self.data.get(username, [])
        for entry in user_entries:
            if entry["name"] == name:
                entry['history'].append(entry['password'])
                entry['password'] = new_password
                self.save_data()
                return

    def delete_password(self, username: str, name: str):
        user_entries = self.data.get(username, [])
        self.data[username] = [entry for entry in user_entries if entry["name"] != name]
        self.save_data()
