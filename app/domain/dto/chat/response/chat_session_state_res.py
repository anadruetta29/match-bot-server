from app.domain.entities.chat_session_state import ChatSessionState
from app.domain.entities.question import Question

class ChatSessionResponse:
    def __init__(self, session_id: str, status: str, step: int, question: dict | None):
        self.session_id = session_id
        self.status = status
        self.step = step
        self.question = question  # ya como dict listo para JSON

    @classmethod
    def from_domain(cls, state: ChatSessionState, current_question: Question | None = None):
        q = current_question or (state.questions[state.step] if state.step < len(state.questions) else None)
        question_dict = {
            "id": q.id,
            "text": q.text,
            "topic": q.topic,
            "options": q.options
        } if q else None

        return cls(
            session_id=state.session.session_id,
            status=state.status,
            step=state.step,
            question=question_dict
        )

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "status": self.status,
            "step": self.step,
            "question": self.question
        }
