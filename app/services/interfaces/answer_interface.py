from typing import Protocol
from app.domain.entities.answer import Answer

class AnswerServiceInterface(Protocol):
    def save_answer(self, session_id: str, answer: Answer) -> None:
        ...
