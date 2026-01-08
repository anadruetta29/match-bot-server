from .session import Session
from .question import Question
from typing import List
from app.domain.entities.chat_status import ChatStatus

class ChatSessionState:
    def __init__(self, session: Session, questions: List[Question], status: ChatStatus, step: int):
        self.session = session
        self.questions = questions
        self.status = status
        self.step = step
