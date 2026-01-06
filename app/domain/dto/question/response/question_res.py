from pydantic import BaseModel
from typing import List
from app.domain.dto.option.response.option_res import OptionResponse

class QuestionResponse(BaseModel):
    id: str
    text: str
    options: List[OptionResponse]
