import json
import os
import uuid
from pathlib import Path

class NoteManager:
    def __init__(self, storage_dir="notes_data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
    def load_notes(self):
        notes = []
        for file_path in self.storage_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    note_data = json.load(f)
                    notes.append(note_data)
            except Exception as e:
                print(f"Error loading note {file_path}: {e}")
        return notes

    def create_note(self, content="", x=100, y=100, width=300, height=300, color="yellow"):
        note_id = str(uuid.uuid4())
        note_data = {
            "id": note_id,
            "content": content,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "color": color
        }
        self.save_note(note_data)
        return note_data

    def save_note(self, note_data):
        file_path = self.storage_dir / f"{note_data['id']}.json"
        with open(file_path, "w") as f:
            json.dump(note_data, f, indent=4)

    def delete_note(self, note_id):
        file_path = self.storage_dir / f"{note_id}.json"
        if file_path.exists():
            file_path.unlink()
