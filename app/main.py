from fastapi import FastAPI, WebSocket, Depends
from app.api.web_socket.chat_handler import ChatWebsocketHandler
from app.config.dependencies import get_chat_processor_step
from app.services.interfaces.process_chat_steps_interface import ProcessChatStepsServiceInterface

app = FastAPI(title="Match Score Bot API")

@app.get("/")
def root():
    return {"status": "Match Score Bot API running"}

@app.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    process_chat_steps: ProcessChatStepsServiceInterface = Depends(get_chat_processor_step)
):

    handler = ChatWebsocketHandler(websocket, process_chat_steps)
    await handler.handle()