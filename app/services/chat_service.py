from app.services.session_service import SessionService
from app.services.score_service import ScoreService
from app.services.question_service import QuestionService
from app.domain.entities.answer import Answer
from app.domain.entities.chat_session_state import ChatSessionState
from app.database.repository.session import SessionRepository
from app.database.repository.answer import AnswerRepository
from app.services.chat_session_state import ChatSessionStateService

import random

session_service = SessionService()
question_service = QuestionService()
score_service = ScoreService()
answer_repository = AnswerRepository()
session_repository = SessionRepository()

chat_session_service = ChatSessionStateService()

class ChatService:
    def __init__(self, num_questions_per_session: int = 10):
        self.num_questions_per_session = num_questions_per_session

    def start_session(self, session_id: str | None) -> ChatSessionState:
        session = session_service.get_or_create(session_id)
        session_repository.create(session.session_id)

        questions = question_service.load()
        selected_questions = random.sample(
            questions,
            k=min(self.num_questions_per_session, len(questions))
        )

        return ChatSessionState(session=session, questions=selected_questions, status="started", step=0)

    def handle_answer(self, state: ChatSessionState, option_id: int | None):
        current_question = chat_session_service.current_question(state)

        if current_question and option_id is not None:
            score = current_question.options[option_id]["score"]
            answer = Answer(
                question_id=current_question.id,
                option_id=option_id,
                score=score
            )
            state.session.add_answer(answer)
            answer_repository.save(state.session.session_id, answer)

        chat_session_service.advance_step(state)
        finished = state.status == "finished"
        next_question = chat_session_service.current_question(state)

        result = None
        if finished:
            raw_score = state.session.get_score().total_score
            max_score_total = sum(
                max(opt["score"] for opt in q.options)
                for q in state.questions
            )
            normalized = score_service._normalize(raw_score, max_score_total)
            session_repository.finish(state.session.session_id, raw_score)
            result = {"score": normalized}

        return next_question, result, finished
