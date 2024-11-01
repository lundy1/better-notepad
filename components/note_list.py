import tkinter as tk
from tkinter import ttk, messagebox
from models.note import Note
from components.editable_label import EditableLabel

class NoteList(tk.Frame):
    def __init__(self, parent, on_note_selected, on_note_deleted):
        super().__init__(parent, bg='#1b2838', width=150)
        self.pack_propagate(False)
        self.on_note_selected = on_note_selected
        self.on_note_deleted = on_note_deleted
        
        header = tk.Frame(self, bg='#1b2838')
        header.pack(fill=tk.X)
        
        self.title_label = EditableLabel(header, text="NOTES", fg='#ffffff', 
                                       bg='#1b2838', font=('Arial', 12, 'bold'))
        self.title_label.pack(side=tk.LEFT, padx=5)
        
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill=tk.X, pady=2)
        
        btn_container = tk.Frame(header, bg='#1b2838')
        btn_container.pack(side=tk.RIGHT, padx=2)
        
        self.add_btn = tk.Button(btn_container, text="+", command=self.add_note,
                               bg='#2a475e', fg='#ffffff', font=('Arial', 12),
                               width=2, relief=tk.FLAT)
        self.add_btn.pack(side=tk.LEFT, padx=1)
        
        self.delete_btn = tk.Button(btn_container, text="🗑", command=self.delete_selected_note,
                                  bg='#2a475e', fg='#ffffff', font=('Arial', 12),
                                  width=2, relief=tk.FLAT)
        self.delete_btn.pack(side=tk.LEFT, padx=1)
        
        self.notes_frame = tk.Frame(self, bg='#1b2838')
        self.notes_frame.pack(fill=tk.BOTH, expand=True)
        
        self.notes = []
        self.note_buttons = []
        self.selected_note = None

    def add_note(self):
        note = Note()
        self.notes.append(note)
        self.create_note_button(note)
        self.select_note(note)

    def create_note_button(self, note):
        btn = tk.Text(self.notes_frame, height=1, wrap=tk.NONE,
                     bg='#2a475e', fg='#ffffff', font=('Arial', 10),
                     relief=tk.FLAT, cursor="hand2")
        btn.insert("1.0", note.title)
        btn.configure(state='disabled')
        
        btn.tag_configure('bold', font=('Arial', 10, 'bold'))
        btn.tag_configure('italic', font=('Arial', 10, 'italic'))
        btn.tag_configure('underline', underline=True)
        
        btn.pack(fill=tk.X, padx=1, pady=1)
        btn.bind('<Button-1>', lambda e: self.select_note(note))
        self.note_buttons.append((note, btn))
        
        for tag in note.title_tags:
            btn.tag_add(tag, "1.0", "end")

    def select_note(self, note):
        self.selected_note = note
        for n, btn in self.note_buttons:
            btn.configure(bg='#2a475e' if n != note else '#3d6a8a')
        self.on_note_selected(note)

    def delete_selected_note(self):
        if self.selected_note and messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            self.notes.remove(self.selected_note)
            for note, btn in self.note_buttons[:]:
                if note == self.selected_note:
                    btn.destroy()
                    self.note_buttons.remove((note, btn))
            self.on_note_deleted()
            if self.notes:
                self.select_note(self.notes[0])
            else:
                self.add_note()

    def update_note_title(self, note, title, tags):
        for n, btn in self.note_buttons:
            if n == note:
                btn.configure(state='normal')
                btn.delete("1.0", tk.END)
                btn.insert("1.0", title)
                
                for tag in ['bold', 'italic', 'underline']:
                    btn.tag_remove(tag, "1.0", tk.END)
                
                for tag in tags:
                    btn.tag_add(tag, "1.0", tk.END)
                
                btn.configure(state='disabled')
                note.title_tags = tags
                break