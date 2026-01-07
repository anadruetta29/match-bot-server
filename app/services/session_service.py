import uuid
from app.domain.entities.session import Session
from app.database.repository.session import SessionRepository
from app.config.exceptions.session_not_found import SessionNotFoundError
from app.services.answer_service import AnswerService
from app.domain.entities.answer import Answer

answer_service = AnswerService()

session_repository = SessionRepository()

_sessions: dict[str, Session] = {}

class SessionService:

    @staticmethod
    def get_or_create(session_id: str | None) -> Session:
        if session_id and session_id in _sessions:
            return _sessions[session_id]

        new_id = str(uuid.uuid4())
        session = Session(session_id=new_id)

        _sessions[new_id] = session
        session_repository.create(session.session_id)

        return session

    @staticmethod
    def add_answer(session_id: str, answer: Answer):
        session = _sessions.get(session_id)
        if not session:
            raise SessionNotFoundError(session_id)

        session.add_answer(answer)

    @staticmethod
    def finish_session(session_id: str):
        session = _sessions.get(session_id)
        if not session:
            raise SessionNotFoundError(session_id)

        session.finish()
        session_repository.finish(session_id)

    @staticmethod
    def get_score(session_id: str):
        session = _sessions.get(session_id)
        if not session:
            return 0
        return session.get_score()
