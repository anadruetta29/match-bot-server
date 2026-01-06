from typing import List
from app.domain.models.answer import Answer

class Score:
    def __init__(self, answers: List[Answer]):
        self.answers = answers

    @property
    def total_score(self) -> int:
        return sum(answer.score for answer in self.answers)
