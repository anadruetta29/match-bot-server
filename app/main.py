from fastapi import FastAPI, WebSocket, Depends
from app.api.web_socket.chat_handler import ChatWebsocketHandler
from app.config.dependencies import get_chat_service
from app.services.interfaces.chat_interface import ChatServiceInterface

app = FastAPI(title="Match Score Bot API")

@app.get("/")
def root():
    return {"status": "Match Score Bot API running"}

@app.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    chat_service: ChatServiceInterface = Depends(get_chat_service)
):

    handler = ChatWebsocketHandler(websocket, chat_service)
    await handler.handle()