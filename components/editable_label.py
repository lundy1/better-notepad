import tkinter as tk

class EditableLabel(tk.Frame):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent)
        self.configure(bg=kwargs.get('bg', '#1b2838'))
        self.text = text
        
        self.label = tk.Label(self, text=self.text, **kwargs)
        self.label.pack(side=tk.LEFT)
        
        self.entry = tk.Entry(self, bg='#2a475e', fg='#ffffff', 
                            font=kwargs.get('font'), relief=tk.FLAT)
        
        self.label.bind('<Double-Button-1>', self.start_edit)
        self.entry.bind('<Return>', self.end_edit)
        self.entry.bind('<FocusOut>', self.end_edit)

    def start_edit(self, event):
        self.label.pack_forget()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.label.cget('text'))
        self.entry.pack(side=tk.LEFT)
        self.entry.focus_set()

    def end_edit(self, event):
        new_text = self.entry.get().strip()
        if new_text:
            self.label.configure(text=new_text)
        self.entry.pack_forget()
        self.label.pack(side=tk.LEFT)