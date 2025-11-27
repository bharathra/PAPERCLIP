
import sys
import os

# Add local libs to path
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

from note_manager import NoteManager
from note_window import NoteWindow

from PyQt6.QtWidgets import QApplication


class PaperClipApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("PaperClip")
        self.app.setDesktopFileName("paperclip.desktop")

        # Use SNAP_USER_DATA if available, otherwise default to "notes_data"
        storage_path = os.environ.get("SNAP_USER_DATA", "notes_data")
        self.manager = NoteManager(storage_dir=storage_path)
        self.windows = {}  # note_id -> NoteWindow

        # Set global window icon
        icon_path = self.get_resource_path("icons/paper_clip_grey.png")
        if os.path.exists(icon_path):
            from PyQt6.QtGui import QIcon
            self.app.setWindowIcon(QIcon(icon_path))

        self.load_notes()

    def get_resource_path(self, relative_path):
        """Get absolute path to resource"""
        snap_root = os.environ.get("SNAP")
        if snap_root:
            return os.path.join(snap_root, "share/paperclip", relative_path)
        return os.path.join(os.path.dirname(__file__), relative_path)

    def load_notes(self):
        notes = self.manager.load_notes()
        if not notes:
            self.create_note()
        else:
            for note_data in notes:
                self.show_note(note_data)

    def create_note(self, x=None, y=None):
        kwargs = {}
        if x is not None:
            kwargs['x'] = x
        if y is not None:
            kwargs['y'] = y

        note_data = self.manager.create_note(**kwargs)
        self.show_note(note_data)

    def show_note(self, note_data):
        window = NoteWindow(note_data)
        window.note_changed.connect(self.manager.save_note)
        window.spawn_requested.connect(self.create_note)
        window.delete_requested.connect(self.on_note_deleted)
        window.closed.connect(self.on_note_closed)

        self.windows[note_data["id"]] = window
        window.show()

    def on_note_closed(self, note_id):
        if note_id in self.windows:
            # We don't delete the file, just remove from active windows list
            del self.windows[note_id]

        if not self.windows:
            self.app.quit()

    def on_note_deleted(self, note_id):
        if note_id in self.windows:
            # Close the window first
            self.windows[note_id].close()
            # The closeEvent will trigger on_note_closed, which removes it from self.windows
            # But we also need to delete the file
            self.manager.delete_note(note_id)

    def run(self):
        sys.exit(self.app.exec())


def main():
    paperclip = PaperClipApp()
    paperclip.run()


if __name__ == "__main__":
    main()
