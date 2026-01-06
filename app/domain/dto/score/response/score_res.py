from pydantic import BaseModel

class ScoreResponse(BaseModel):
    score: int
