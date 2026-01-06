from typing import List, Optional
from app.domain.models.answer import Answer
from app.domain.models.score import Score

class Session:
    def __init__(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        answers: Optional[List[Answer]] = None,
        finished: bool = False,
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.answers = answers or []
        self.finished = finished

    def add_answer(self, answer: Answer):
        self.answers.append(answer)

    def get_score(self) -> Score:
        from app.domain.models.score import Score
        return Score(self.answers)
