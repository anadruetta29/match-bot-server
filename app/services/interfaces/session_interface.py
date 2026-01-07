
from typing import Protocol, Optional
from app.domain.entities.session import Session
from app.domain.entities.answer import Answer
from app.domain.entities.score import Score

class SessionServiceInterface(Protocol):
    def get_or_create(self, session_id: Optional[str]) -> Session:
        ...

    def add_answer(self, session_id: str, answer: Answer) -> None:
        ...

    def finish_session(self, session_id: str, final_score: int) -> None:
        ...

    def get_score(self, session_id: str) -> Score:
        ...
