from pydantic import BaseModel

class AnswerRequest(BaseModel):
    question_id: str
    option_id: int
    score: int