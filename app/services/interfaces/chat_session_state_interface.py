from typing import Protocol, Optional
from app.domain.entities.chat_session_state import ChatSessionState
from app.domain.entities.question import Question

class ChatSessionStateServiceInterface(Protocol):
    def current_question(self, state: ChatSessionState) -> Optional[Question]:
        ...

    def advance_step(self, state: ChatSessionState) -> None:
        ...

    def is_finished(self, state: ChatSessionState) -> bool:
        ...
