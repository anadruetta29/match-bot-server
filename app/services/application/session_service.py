import uuid
from app.domain.entities.session import Session
from app.database.repository.session import SessionRepository
from app.config.exceptions.session_not_found import SessionNotFoundError

from app.services.interfaces.answer_interface import AnswerServiceInterface

from app.domain.entities.answer import Answer

session_repository: SessionRepository = SessionRepository()

_sessions: dict[str, Session] = {}

class SessionService:
    def __init__(
        self,
        answer_service: AnswerServiceInterface,
    ):
        self.answer_service = answer_service

    def get_or_create(self, session_id: str | None) -> Session:
        if session_id and session_id in _sessions:
            return _sessions[session_id]

        new_id = str(uuid.uuid4())
        session = Session(session_id=new_id)

        _sessions[new_id] = session
        session_repository.create(session.session_id)

        return session

    def add_answer(self, session_id: str, answer: Answer):
        session = _sessions.get(session_id)
        if not session:
            raise SessionNotFoundError(session_id)

        session.add_answer(answer)
        self.answer_service.save_answer(session_id, answer)

    def finish_session(self, session_id: str, final_score: int, features: dict):
        session = _sessions.get(session_id)
        if not session:
            raise SessionNotFoundError(session_id)

        session.finish()
        session.features = features
        session_repository.finish(session_id, final_score, features)

    @staticmethod
    def get_score(session_id: str):
        session = _sessions.get(session_id)
        if not session:
            return 0
        return session.get_score()

    def update_feedback(self, session_id: str, is_useful: bool):
        session_repository.update_feedback(session_id, is_useful)