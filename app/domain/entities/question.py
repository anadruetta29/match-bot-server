from typing import List, Optional
from app.domain.entities.option import Option

class Question:
    def __init__(self, id: str, text: str, topic: str, options: Optional[List[Option]] = None):
        self.id = id
        self.text = text
        self.topic = topic
        self.options = options or []
