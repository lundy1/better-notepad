import tkinter as tk
import re

class Editor(tk.Frame):
    def __init__(self, parent, on_text_changed):
        super().__init__(parent, bg='#1b2838')
        self.on_text_changed = on_text_changed
        
        self.toolbar = tk.Frame(self, bg='#2a475e')
        self.toolbar.pack(fill=tk.X, pady=(0, 1))
        
        button_font = ('Arial', 16, 'bold')
        buttons = [
            ("B", self.toggle_bold, "Bold (Ctrl+B)"),
            ("I", self.toggle_italic, "Italic (Ctrl+I)"),
            ("U", self.toggle_underline, "Underline (Ctrl+U)"),
            ("```", self.insert_code_block, "Code Block (Ctrl+K)"),
            ("=", self.calculate_formula, "Calculate (=)")
        ]
        
        for text, command, tooltip in buttons:
            btn = tk.Button(self.toolbar, text=text, command=command,
                          bg='#2a475e', fg='#ffffff', relief=tk.FLAT,
                          font=button_font, width=3, height=1)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.create_tooltip(btn, tooltip)
        
        self.text_editor = tk.Text(self, wrap=tk.WORD, bg='#171d25', fg='#ffffff',
                                 insertbackground='#ffffff', relief=tk.FLAT,
                                 font=('Consolas', 11))
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.text_editor.tag_configure('bold', font=('Consolas', 11, 'bold'))
        self.text_editor.tag_configure('italic', font=('Consolas', 11, 'italic'))
        self.text_editor.tag_configure('underline', underline=True)
        self.text_editor.tag_configure('code', background='#2a2e33', foreground='#e6db74',
                                     font=('Consolas', 11), spacing1=5, spacing3=5)
        
        self.text_editor.bind('<<Modified>>', self.on_text_change)
        self.text_editor.bind('<KeyRelease>', self.on_key_release)
        self.text_editor.bind('<Control-b>', lambda e: self.toggle_bold())
        self.text_editor.bind('<Control-i>', lambda e: self.toggle_italic())
        self.text_editor.bind('<Control-u>', lambda e: self.toggle_underline())
        self.text_editor.bind('<Control-k>', lambda e: self.insert_code_block())

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, bg='#2a475e', fg='white',
                           relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.after(2000, hide_tooltip)
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def toggle_bold(self, event=None):
        self.toggle_tag('bold')
        return 'break'

    def toggle_italic(self, event=None):
        self.toggle_tag('italic')
        return 'break'

    def toggle_underline(self, event=None):
        self.toggle_tag('underline')
        return 'break'

    def toggle_tag(self, tag_name):
        try:
            if self.text_editor.tag_ranges(tk.SEL):
                ranges = self.text_editor.tag_ranges(tk.SEL)
                if tag_name in self.text_editor.tag_names(ranges[0]):
                    self.text_editor.tag_remove(tag_name, *ranges)
                else:
                    self.text_editor.tag_add(tag_name, *ranges)
        except tk.TclError:
            pass

    def insert_code_block(self, event=None):
        try:
            if self.text_editor.tag_ranges(tk.SEL):
                selected_text = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.text_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self.text_editor.insert(tk.INSERT, f"\n```\n{selected_text}\n```\n")
                start = self.text_editor.index("insert-2l linestart")
                end = self.text_editor.index("insert-1l lineend+1c")
                self.text_editor.tag_add('code', start, end)
            else:
                self.text_editor.insert(tk.INSERT, "\n```\n\n```\n")
                start = self.text_editor.index("insert-2l linestart")
                end = self.text_editor.index("insert lineend+1c")
                self.text_editor.tag_add('code', start, end)
                self.text_editor.mark_set(tk.INSERT, "insert-2l")
        except tk.TclError:
            pass
        return 'break'

    def calculate_formula(self, event=None):
        try:
            if self.text_editor.tag_ranges(tk.SEL):
                selected_text = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            else:
                line = self.text_editor.get("insert linestart", "insert lineend")
                selected_text = line
            
            if '=' not in selected_text:
                return 'break'
            
            expression = selected_text.split('=')[0].strip()
            expression = re.sub(r'\s+', '', expression)
            
            try:
                if re.match(r'^[\d+\-*/().]+$', expression):
                    result = eval(expression)
                    formatted_result = f"{expression} = {result}"
                    if self.text_editor.tag_ranges(tk.SEL):
                        self.text_editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                        self.text_editor.insert(tk.INSERT, formatted_result)
                    else:
                        self.text_editor.delete("insert linestart", "insert lineend")
                        self.text_editor.insert("insert linestart", formatted_result)
            except:
                pass
        except tk.TclError:
            pass
        return 'break'

    def on_key_release(self, event):
        if event.char == '=' and not event.state & 0x4:
            self.calculate_formula()

    def get_content(self):
        return self.text_editor.get("1.0", tk.END)

    def get_first_line_tags(self):
        tags = []
        for tag in ['bold', 'italic', 'underline']:
            ranges = self.text_editor.tag_ranges(tag)
            if ranges and self.text_editor.compare(ranges[0], "<=", "1.end"):
                tags.append(tag)
        return tags

    def set_content(self, content):
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert("1.0", content)

    def on_text_change(self, event):
        content = self.get_content()
        title = content.split('\n')[0].strip() or "Untitled Note"
        tags = self.get_first_line_tags()
        self.on_text_changed(content, title, tags)
        self.text_editor.edit_modified(False)