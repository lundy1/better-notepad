from datetime import datetime

class Note:
    def __init__(self, title="Untitled Note", content="", title_tags=None):
        self.title = title
        self.content = content
        self.title_tags = title_tags or []
        self.last_modified = datetime.now().isoformat()