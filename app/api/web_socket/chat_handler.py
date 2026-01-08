from app.services.interfaces.chat_interface import ChatServiceInterface
from fastapi import WebSocket, WebSocketDisconnect

from app.resources.welcome_message import WELCOME_MESSAGE

class ChatWebsocketHandler:
    def __init__(self, websocket: WebSocket, chat_service: ChatServiceInterface):
        self.websocket = websocket
        self.chat_service = chat_service
        self.state = None

    async def handle(self):
        await self.websocket.accept()
        await self.websocket.send_json(WELCOME_MESSAGE)

        try:
            while True:
                data = await self.websocket.receive_json()

                result = self.chat_service.process_message(data, self.state)

                self.state = result["new_state"]

                await self.websocket.send_json(result["response"])

                if result["should_close"]:
                    break
        except WebSocketDisconnect:
            pass
        finally:
            await self.websocket.close()