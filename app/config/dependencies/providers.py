from app.services.interfaces.answer_interface import AnswerServiceInterface
from app.services.interfaces.chat_interface import ChatServiceInterface
from app.services.interfaces.chat_session_state_interface import ChatSessionStateServiceInterface
from app.services.interfaces.question_interface import QuestionServiceInterface
from app.services.interfaces.score_interface import ScoreServiceInterface
from app.services.interfaces.session_interface import SessionServiceInterface
from app.services.interfaces.process_chat_steps_interface import ProcessChatStepsServiceInterface

def get_session_service() -> "SessionServiceInterface":
    from app.services.application.session_service import SessionService
    return SessionService()

def get_question_service() -> "QuestionServiceInterface":
    from app.services.application.question_service import QuestionService
    return QuestionService()

def get_score_service() -> "ScoreServiceInterface":
    from app.services.application.score_service import ScoreService
    return ScoreService()

def get_chat_session_state_service() -> "ChatSessionStateServiceInterface":
    from app.services.application.chat_session_state import ChatSessionStateService
    return ChatSessionStateService()

def get_chat_service() -> "ChatServiceInterface":
    from app.services.application.chat_service import ChatService
    return ChatService(
        session_service=get_session_service(),
        question_service=get_question_service(),
        score_service=get_score_service(),
        chat_session_service=get_chat_session_state_service()
    )

def get_chat_processor_step() -> ProcessChatStepsServiceInterface:
    from app.services.application.process_chat_steps import ProcessChatSteps
    return ProcessChatSteps(
        chat_service=get_chat_service()
    )

def get_answer_service() -> "AnswerServiceInterface":
    from app.services.application.answer_service import AnswerService
    return AnswerService()

