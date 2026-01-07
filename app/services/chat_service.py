from app.services.session_service import SessionService
from app.services.score_service import ScoreService
from app.services.question_service import QuestionService
from app.domain.entities.answer import Answer
from app.domain.entities.chat_session_state import ChatSessionState
from app.database.repository.answer import AnswerRepository
from app.services.chat_session_state import ChatSessionStateService
from app.config.exceptions.invalid_option import InvalidOptionError
import random

session_service = SessionService()
question_service = QuestionService()
score_service = ScoreService()
chat_session_service = ChatSessionStateService()

class ChatService:
    def __init__(self, questions_per_session: int = 10):
        self.questions_per_session = questions_per_session

    def start_session(self, session_id: str | None) -> ChatSessionState:
        session = session_service.get_or_create(session_id)

        questions = question_service.load()
        selected_questions = random.sample(
            questions,
            k=min(self.questions_per_session, len(questions))
        )

        return ChatSessionState(
            session=session,
            questions=selected_questions,
            status="started",
            step=0
        )

    def handle_answer(self, state: ChatSessionState, option_id: int | None):
        current_question = chat_session_service.current_question(state)

        if option_id is None or option_id < 0 or option_id >= len(current_question.options):
            raise InvalidOptionError(option_id)

        score = current_question.options[option_id]["score"]
        answer = Answer(
            question_id=current_question.id,
            option_id=option_id,
            score=score
        )

        session_service.add_answer(state.session.session_id, answer)

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

            session_service.finish_session(state.session.session_id)

            result = {"score": normalized}

        return next_question, result, finished
