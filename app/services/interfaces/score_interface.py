from typing import Protocol, List
from app.domain.entities.answer import Answer
from app.domain.entities.question import Question

class ScoreServiceInterface(Protocol):
    def calculate_final_score(
        self,
        answers: List[Answer],
        questions: List[Question]
    ) -> int:
        ...

    def _scale(self, raw: int, max_score: int):
        ...