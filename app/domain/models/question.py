from typing import List, Optional
from app.domain.models.option import Option

class Question:
    def __init__(self, id: str, text: str, options: Optional[List[Option]] = None):
        self.id = id
        self.text = text
        self.options = options or []
