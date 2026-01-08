from app.services.interfaces.session_interface import SessionServiceInterface
from app.services.interfaces.question_interface import QuestionServiceInterface
from app.services.interfaces.score_interface import ScoreServiceInterface
from app.services.interfaces.chat_session_state_interface import ChatSessionStateServiceInterface

from app.domain.dto.chat.response.chat_session_state_res import ChatSessionStateResponse

from app.domain.entities.chat_session_state import ChatSessionState
from app.domain.entities.answer import Answer

from app.config.exceptions.invalid_option import InvalidOptionError

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
            status="started",
            step=0
        )

    def handle_answer(self, state: ChatSessionState, option_id: int | None):
        current_question = self.chat_session_service.current_question(state)

        if option_id is None or option_id < 0 or option_id >= len(current_question.options):
            raise InvalidOptionError(option_id)

        selected_option = current_question.options[option_id]

        answer = Answer(
            question_id=current_question.id,
            option_id=option_id,
            score=selected_option["score"]
        )

        self.session_service.add_answer(state.session.session_id, answer)

        self.chat_session_service.advance_step(state)

        finished = state.status == "finished"
        next_question = self.chat_session_service.current_question(state)

        result = None
        if finished:
            final_score = self.score_service.calculate_final_score(
                state.session.answers,
                state.questions
            )

            self.session_service.finish_session(
                state.session.session_id,
                final_score
            )

            result = {"score": final_score}

        return next_question, result, finished

    def process_message(self, data: dict, current_state: ChatSessionState | None):

        option_id = data.get("option_id")
        session_id = data.get("session_id")

        if current_state is None:
            if option_id == 0:
                new_state = self.start_session(session_id)
                chat_res = ChatSessionStateResponse.from_domain(new_state)
                return {
                    "response": chat_res.to_dict(),
                    "new_state": new_state,
                    "should_close": False
                }
            else:
                return {
                    "response": {"finished": True, "result": {"score": 0}},
                    "new_state": None,
                    "should_close": True
                }

        try:
            next_q, result, finished = self.handle_answer(current_state, option_id)
            chat_res = ChatSessionStateResponse.from_domain(current_state, next_q)

            return {
                "response": {
                    "session": chat_res.to_dict(),
                    "result": result,
                    "finished": finished
                },
                "new_state": current_state,
                "should_close": finished
            }
        except InvalidOptionError as e:
            return {
                "response": {"error": str(e)},
                "new_state": current_state,
                "should_close": False
            }
