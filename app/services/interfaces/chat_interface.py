from typing import Protocol, Tuple, Optional
from app.domain.entities.chat_session_state import ChatSessionState
from app.domain.entities.question import Question

class ChatServiceInterface(Protocol):
    def start_session(self, session_id: Optional[str]) -> ChatSessionState:
        ...

    def handle_answer(
        self,
        state: ChatSessionState,
        option_id: Optional[int]
    ) -> Tuple[Optional[Question], Optional[dict], bool]:
        ...