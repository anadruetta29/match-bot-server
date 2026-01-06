from typing import Optional
from app.domain.models.question import Question
from app.domain.models.score import Score

class Chat:
    def __init__(
        self,
        session_id: str,
        question: Optional[Question] = None,
        result: Optional[Score] = None,
        finished: bool = False
    ):
        self.session_id = session_id
        self.question = question
        self.result = result
        self.finished = finished
