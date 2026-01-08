
from typing import Protocol, List
from app.domain.entities.question import Question

class QuestionServiceInterface(Protocol):
    def load(self) -> List[Question]:
        ...
