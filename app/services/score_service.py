class ScoreService:
    MIN_SCORE = 1
    MAX_SCORE = 10

    def calculate(self, answers, selected_questions):
        raw_score = sum(answer.score for answer in answers)
        max_score_total = sum(max(opt["score"] for opt in q["options"]) for q in selected_questions)
        return self._normalize(raw_score, max_score_total)

    def _normalize(self, raw_score: int, max_score_total: int) -> int:
        if max_score_total == 0:
            return self.MIN_SCORE
        normalized = raw_score / max_score_total
        scaled = self.MIN_SCORE + normalized * (self.MAX_SCORE - self.MIN_SCORE)
        return round(scaled)
