from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.services.chat_service import ChatService
from app.services.chat_session_state import ChatSessionStateService
from app.domain.dto.chat.response.chat_session_state_res import ChatSessionResponse
from app.config.exceptions.invalid_option import InvalidOptionError
app = FastAPI(title="Match Score Bot API")
chat_service = ChatService()
chat_session_service = ChatSessionStateService()

@app.get("/")
def root():
    return {"status": "Match Score Bot API running"}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session_state = None
    started = False

    welcome_message = {
        "session_id": None,
        "question": {
            "id": "welcome",
            "text": "¡Hola! Gracias por venir a buscar consejo en mí, ¿Estás listo para saber si es un buen match?",
            "options": [
                {"id": 0, "label": "Sí"},
                {"id": 1, "label": "No"}
            ]
        },
        "result": None,
        "finished": False
    }
    await websocket.send_json(welcome_message)

    try:
        while True:
            data = await websocket.receive_json()
            option_id = data.get("option_id")
            session_id = data.get("session_id")

            if not started:
                if option_id == 0:
                    session_state = chat_service.start_session(session_id)
                    started = True
                    chat_response = ChatSessionResponse.from_domain(session_state)
                    await websocket.send_json(chat_response.to_dict())
                    continue
                else:
                    await websocket.send_json({
                        "session_id": session_id,
                        "question": None,
                        "result": {"score": 0},
                        "finished": True
                    })
                    await websocket.close()
                    break

            try:
                next_question, result, finished = chat_service.handle_answer(session_state, option_id)
            except InvalidOptionError as e:
                current_q = chat_session_service.current_question(session_state)
                chat_response = ChatSessionResponse.from_domain(session_state, current_q)
                await websocket.send_json({
                    "error": str(e),
                    "session": chat_response.to_dict()
                })
                continue

            chat_response = ChatSessionResponse.from_domain(session_state, next_question)
            await websocket.send_json({
                "session": chat_response.to_dict(),
                "result": result,
                "finished": finished
            })

            if finished:
                await websocket.close()
                break

    except WebSocketDisconnect:
        print(f"Cliente desconectado: {session_state.session.session_id if session_state else 'desconocido'}")
