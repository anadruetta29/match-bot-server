from app.domain.entities.question import Question
import json
from pathlib import Path

DATASET_PATH = Path("data/dataset.json")

class QuestionService:
    _questions: list[Question] | None = None

    @classmethod
    def load(cls) -> list[Question]:
        if cls._questions is None:
            with open(DATASET_PATH, "r", encoding="utf-8") as f:
                raw_questions = json.load(f)
                cls._questions = [
                    Question(
                        id=q["id"],
                        text=q["text"],
                        topic=q["topic"],
                        options=q["options"]
                    )
                    for q in raw_questions
                ]
        return cls._questions
