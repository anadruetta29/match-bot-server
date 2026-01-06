from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.services.chat_service import ChatService

app = FastAPI(title="Match Score Bot API")
chat_service = ChatService()

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session = None
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
                if option_id == 0:  # Sí
                    session = chat_service.start_session(session_id)
                    started = True
                else:
                    await websocket.send_json({
                        "session_id": session_id,
                        "question": None,
                        "result": {"score": 0},
                        "finished": True
                    })
                    await websocket.close()
                    break

            next_question, result, finished = chat_service.handle_answer(session, option_id)

            await websocket.send_json({
                "session_id": session.session_id,
                "question": next_question,
                "result": result,
                "finished": finished
            })

            if finished:
                await websocket.close()
                break

    except WebSocketDisconnect:
        print(f"Cliente desconectado: {session.session_id if session else 'desconocido'}")
