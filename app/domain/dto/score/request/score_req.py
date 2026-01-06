from pydantic import BaseModel
from typing import List
from answer_req import AnswerRequest

class ScoreRequest(BaseModel):
    answers: List[AnswerRequest]
