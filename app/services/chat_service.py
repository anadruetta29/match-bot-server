from app.services.session_service import SessionService
from app.services.score_service import ScoreService
from app.services.question_service import QuestionService
from app.domain.models.answer import Answer
import random

score_service = ScoreService()
session_service = SessionService()
question_service = QuestionService()


class ChatService:
    def __init__(self):
        self.num_questions_per_session = 10

    def start_session(self, session_id: str | None):
        session = session_service.get_or_create(session_id)

        questions = question_service.load()
        num_questions = min(self.num_questions_per_session, len(questions))
        selected_questions = random.sample(questions, k=num_questions)
        session.selected_questions = selected_questions
        session.step = 0
        return session

    def handle_answer(self, session: "Session", option_id: int | None):

        if session.step > 0 and option_id is not None:
            prev_question = session.selected_questions[session.step - 1]
            score = prev_question["options"][option_id]["score"]
            answer = Answer(
                question_id=prev_question["id"],
                option_id=option_id,
                score=score
            )
            session.add_answer(answer)

        finished = session.step >= len(session.selected_questions)

        next_question = None
        if not finished:
            next_question = session.selected_questions[session.step]
            session.step += 1

        result = None
        if finished:
            raw_score = session.get_score().total_score

            max_score_total = sum(max(opt["score"] for opt in q["options"]) for q in session.selected_questions)
            normalized_score = score_service._normalize(raw_score, max_score_total)
            result = {"score": normalized_score}

        return next_question, result, finished
