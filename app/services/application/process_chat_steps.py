from app.services.interfaces.chat_interface import ChatServiceInterface
from app.domain.entities.chat_session_state import ChatSessionState
from app.domain.dto.chat.response.chat_session_state_res import ChatSessionStateResponse
from app.config.exceptions.invalid_option import InvalidOptionError

from app.domain.entities.chat_status import ChatStatus


class ProcessChatSteps:

    def __init__(self, chat_service: ChatServiceInterface):
        self.chat_service = chat_service

    def execute(self, data: dict, current_state: ChatSessionState | None):
        option_id = data.get("option_id")
        session_id = data.get("session_id")

        if current_state is None:
            return self._handle_initial_contact(session_id, option_id)

        return self._handle_ongoing_chat(current_state, option_id)

    def _handle_initial_contact(self, session_id, option_id):
        if option_id == 0:
            new_state = self.chat_service.start_session(session_id)
            res = ChatSessionStateResponse.from_domain(new_state)

            return {
                "response": res.to_dict(),
                "new_state": new_state,
                "should_close": new_state.status == ChatStatus.FINISHED
            }

        return {
            "response": {"finished": True, "result": {"score": 0}},
            "new_state": None,
            "should_close": True
        }

    def _handle_ongoing_chat(self, state, option_id):
        try:

            next_q, result, finished = self.chat_service.handle_answer(state, option_id)

            res = ChatSessionStateResponse.from_domain(state, next_q)
            return {
                "response": {"session": res.to_dict(), "result": result, "finished": finished},
                "new_state": state,
                "should_close": finished
            }
        except InvalidOptionError as e:
            return {"response": {"error": str(e)}, "new_state": state, "should_close": False}