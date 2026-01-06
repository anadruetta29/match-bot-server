from pydantic import BaseModel
from typing import Optional
from app.domain.dto.question.response.question_res import QuestionResponse
from app.domain.dto.score.response.score_res import ScoreResponse

class ChatResponse(BaseModel):
    session_id: str
    question: Optional[QuestionResponse] = None
    result: Optional[ScoreResponse] = None
    finished: bool
