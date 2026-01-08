from app.services.interfaces.session_interface import SessionServiceInterface
from app.services.interfaces.question_interface import QuestionServiceInterface
from app.services.interfaces.score_interface import ScoreServiceInterface
from app.services.interfaces.chat_session_state_interface import ChatSessionStateServiceInterface

from app.domain.entities.chat_session_state import ChatSessionState
from app.domain.entities.answer import Answer

from app.config.exceptions.invalid_option import InvalidOptionError

from app.domain.entities.chat_status import ChatStatus

import random

class ChatService:
    def __init__(
        self,
        session_service: SessionServiceInterface,
        question_service: QuestionServiceInterface,
        score_service: ScoreServiceInterface,
        chat_session_service: ChatSessionStateServiceInterface,
        questions_per_session: int = 10
    ):
        self.session_service = session_service
        self.question_service = question_service
        self.score_service = score_service
        self.chat_session_service = chat_session_service
        self.questions_per_session = questions_per_session

    def start_session(self, session_id: str | None) -> ChatSessionState:
        session = self.session_service.get_or_create(session_id)

        questions = self.question_service.load()
        selected_questions = random.sample(
            questions,
            k=min(self.questions_per_session, len(questions))
        )

        return ChatSessionState(
            session=session,
            questions=selected_questions,
            status=ChatStatus.STARTED,
            step=0
        )

    def handle_answer(self, state: ChatSessionState, option_id: int | None):
        current_question = self.chat_session_service.current_question(state)

        if option_id is None or option_id < 0 or option_id >= len(current_question.options):
            raise InvalidOptionError(option_id)

        selected_option = current_question.options[option_id]

        answer = Answer(
            question_id=current_question.id,
            question_text=current_question.text,
            topic=current_question.topic,
            option_id=option_id,
            option_text=selected_option["label"],
            score=selected_option["score"]
        )

        self.session_service.add_answer(state.session.session_id, answer)

        self.chat_session_service.advance_step(state)

        finished = state.status == ChatStatus.FINISHED
        next_question = self.chat_session_service.current_question(state)

        result = None
        if finished:
            calculation = self.score_service.calculate_final_score(
                state.session.answers,
                state.questions
            )

            self.session_service.finish_session(
                state.session.session_id,
                final_score=calculation["score"],
                features=calculation["features"]
            )

            result = {
                "score": calculation["score"],
                "session_id": state.session.session_id,
                "message": "¿Te fue útil este consejo?"
            }

        return next_question, result, finished


