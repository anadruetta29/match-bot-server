from app.domain.entities.chat_session_state import ChatSessionState
from app.domain.entities.question import Question

from typing import Optional

from app.domain.entities.chat_status import ChatStatus


class ChatSessionStateService:
    @staticmethod
    def current_question(state: ChatSessionState) -> Optional[Question]:
        if state.step < len(state.questions):
            return state.questions[state.step]
        return None

    @staticmethod
    def advance_step(state: ChatSessionState):
        state.step += 1
        if state.step >= len(state.questions):
            state.status = ChatStatus.FINISHED

    @staticmethod
    def is_finished(state: ChatSessionState) -> bool:
        return state.status == ChatStatus.FINISHED
