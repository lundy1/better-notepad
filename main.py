import tkinter as tk
from components.note_list import NoteList
from components.editor import Editor
from models.note import Note
import json
import os

class BetterNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Better Notepad")
        self.root.configure(bg='#1b2838')
        
        main_container = tk.Frame(root, bg='#1b2838')
        main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.note_list = NoteList(main_container, self.on_note_selected, self.on_note_deleted)
        self.note_list.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
        
        self.editor = Editor(main_container, self.on_text_changed)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.load_notes()
        if not self.note_list.notes:
            self.note_list.add_note()

    def load_notes(self):
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r') as f:
                    notes_data = json.load(f)
                    for note_data in notes_data:
                        note = Note(
                            note_data['title'],
                            note_data['content'],
                            note_data.get('title_tags', [])
                        )
                        self.note_list.notes.append(note)
                        self.note_list.create_note_button(note)
        except:
            pass

    def save_notes(self):
        notes_data = [{
            'title': note.title,
            'content': note.content,
            'title_tags': note.title_tags
        } for note in self.note_list.notes]
        with open('notes.json', 'w') as f:
            json.dump(notes_data, f)

    def on_note_selected(self, note):
        self.editor.set_content(note.content)

    def on_note_deleted(self):
        self.save_notes()

    def on_text_changed(self, content, title, tags):
        if self.note_list.selected_note:
            self.note_list.selected_note.content = content
            self.note_list.selected_note.title = title
            self.note_list.update_note_title(self.note_list.selected_note, title, tags)
            self.save_notes()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = BetterNotepad(root)
    root.mainloop()