from typing import Protocol
from app.domain.entities.chat_session_state import ChatSessionState

class ProcessChatStepsServiceInterface(Protocol):

    def execute(self, data: dict, current_state: ChatSessionState | None):
        ...

    def _handle_initial_contact(self, session_id, option_id):
        ...

    def _handle_ongoing_chat(self, state, option_id):
        ...
