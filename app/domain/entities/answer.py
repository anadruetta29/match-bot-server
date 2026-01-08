class Answer:
    def __init__(
        self, 
        question_id: str, 
        question_text: str,
        topic: str,
        option_id: int, 
        option_text: str,
        score: int
    ):
        self.question_id = question_id
        self.question_text = question_text
        self.topic = topic
        self.option_id = option_id
        self.option_text = option_text
        self.score = score