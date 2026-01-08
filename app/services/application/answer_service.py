from app.database.repository.answer import AnswerRepository
from app.domain.entities.answer import Answer

answer_repository = AnswerRepository()

class AnswerService:

    @staticmethod
    def save_answer(session_id: str, answer: Answer):
        answer_repository.save(session_id, answer)
