from fastapi import FastAPI, WebSocket, Depends
from app.api.web_socket.chat_handler import ChatWebsocketHandler
from app.config.dependencies import get_chat_processor_step, get_session_service
from app.services.interfaces.process_chat_steps_interface import ProcessChatStepsServiceInterface
from app.services.interfaces.session_interface import SessionServiceInterface

app = FastAPI(title="Match Score Bot API")

@app.get("/")
def root():
    return {"status": "Match Score Bot API running"}

@app.post("/sessions/{session_id}/feedback")
async def set_feedback(
        session_id: str,
        is_useful: bool,
        session_service: SessionServiceInterface = Depends(get_session_service)
):

    session_service.update_feedback(session_id, is_useful)
    return {"status": "ok"}

@app.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    process_chat_steps: ProcessChatStepsServiceInterface = Depends(get_chat_processor_step)
):

    handler = ChatWebsocketHandler(websocket, process_chat_steps)
    await handler.handle()