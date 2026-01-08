from app.database.session import SessionLocal
from app.database.models.answer import AnswerModel


class AnswerRepository:

    def save(self, session_id: str, answer):
        db = SessionLocal()
        try:
            db_answer = AnswerModel(
                session_id=session_id,
                question_id=answer.question_id,
                question_text=answer.question_text,
                topic=answer.topic,
                option_id=answer.option_id,
                option_text=answer.option_text,
                score=answer.score
            )
            db.add(db_answer)
            db.commit()
        finally:
            db.close()
