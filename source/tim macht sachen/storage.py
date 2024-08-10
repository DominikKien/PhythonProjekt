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

    def add_password(self, username: str, password: str, notes: str = "", category: str = ""):
        entry = {
            "username": username,
            "password": password,
            "notes": notes,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "history": []
        }
        self.data[username] = entry
        self.save_data()

    def get_password(self, username: str) -> Dict:
        return self.data.get(username)

    def update_password(self, username: str, new_password: str):
        entry = self.data.get(username)
        if entry:
            entry['history'].append(entry['password'])
            entry['password'] = new_password
            self.save_data()

    def delete_password(self, username: str):
        if username in self.data:
            del self.data[username]
            self.save_data()
