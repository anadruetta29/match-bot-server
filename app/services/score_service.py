class ScoreService:
    MIN_SCORE = 1
    MAX_SCORE = 10

    def calculate_final_score(self, answers, questions) -> int:
        raw_score = sum(a.score for a in answers)
        max_score = sum(
            max(opt["score"] for opt in q.options)
            for q in questions
        )
        return self._scale(raw_score, max_score)

    def _scale(self, raw: int, max_score: int) -> int:
        if max_score == 0:
            return self.MIN_SCORE
        normalized = raw / max_score
        scaled = self.MIN_SCORE + normalized * (self.MAX_SCORE - self.MIN_SCORE)
        return round(scaled)
