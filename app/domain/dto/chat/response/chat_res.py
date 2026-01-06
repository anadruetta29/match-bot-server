from pydantic import BaseModel

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    score: int | None = None
    finished: bool = False
