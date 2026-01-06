from pydantic import BaseModel

class OptionResponse(BaseModel):
    id: int
    label: str
