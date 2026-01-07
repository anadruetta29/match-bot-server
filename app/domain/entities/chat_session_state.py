from .session import Session
from .question import Question
from typing import List

class ChatSessionState:
    def __init__(self, session: Session, questions: List[Question], status: str, step: int):
        self.session = session
        self.questions = questions
        self.status = status
        self.step = step
