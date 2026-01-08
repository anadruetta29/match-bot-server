from app.database.session import SessionLocal
from app.database.models.session import SessionModel
from app.config.exceptions.session_not_found import SessionNotFoundError
from datetime import datetime, UTC


class SessionRepository:

    def create(self, session_id: str):
        db = SessionLocal()
        try:
            session = SessionModel(id=session_id)
            db.add(session)
            db.commit()
        finally:
            db.close()

    def finish(self, session_id: str, final_score: int, features: dict):
        db = SessionLocal()
        try:
            session = db.query(SessionModel).filter_by(id=session_id).first()
            if not session:
                raise SessionNotFoundError(session_id)

            session.finished_at = datetime.now(UTC)

            session.total_score = final_score

            session.features = features

            db.commit()
        finally:
            db.close()

    def update_feedback(self, session_id: str, is_useful: bool):
        db = SessionLocal()
        try:
            session = db.query(SessionModel).filter_by(id=session_id).first()
            if session:
                session.user_feedback = is_useful
                db.commit()
        finally:
            db.close()
