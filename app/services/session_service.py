import uuid
from app.domain.models.session import Session

_sessions: dict[str, Session] = {}

class SessionService:

    @staticmethod
    def get_or_create(session_id: str | None) -> Session:
        if session_id and session_id in _sessions:
            return _sessions[session_id]

        new_id = str(uuid.uuid4())
        session = Session(session_id=new_id)
        _sessions[new_id] = session
        return session

    @staticmethod
    def add_answer(session_id: str, question_id: str, option_id: int, score: int):
        session = _sessions.get(session_id)
        if not session:
            session_id, session = SessionService.get_or_create(None)

        from app.domain.models.answer import Answer
        answer = Answer(question_id=question_id, option_id=option_id, score=score)
        session.add_answer(answer)

    @staticmethod
    def get_score(session_id: str):
        session = _sessions.get(session_id)
        if not session:
            return 0
        return session.get_score()
