from typing import Optional
from app.domain.entities.question import Question
from app.domain.entities.score import Score

class Chat:
    def __init__(
        self,
        session_id: str,
        question: Optional[Question] = None,
        result: Optional[dict] = None,
        finished: bool = False
    ):
        self.session_id = session_id
        self.question = question
        self.result = result
        self.finished = finished
