# app/services/application/score_service.py

class ScoreService:
    MIN_SCORE = 1
    MAX_SCORE = 10

    def calculate_final_score(self, answers, questions) -> dict:

        questions_map = {q.id: q for q in questions}

        topic_scores = {}
        total_raw = 0
        total_max = 0

        for ans in answers:
            question = questions_map.get(ans.question_id)
            if not question:
                continue

            topic = question.topic
            if topic not in topic_scores:
                topic_scores[topic] = {"raw": 0, "max": 0}

            topic_scores[topic]["raw"] += ans.score
            total_raw += ans.score

            max_puntos_q = max(opt["score"] for opt in question.options)
            topic_scores[topic]["max"] += max_puntos_q
            total_max += max_puntos_q

        features = {}
        for topic, values in topic_scores.items():
            if values["max"] > 0:
                features[topic] = round(values["raw"] / values["max"], 2)
            else:
                features[topic] = 0.0

        final_scaled_score = self._scale(total_raw, total_max)

        return {
            "score": final_scaled_score,
            "features": features
        }

    def _scale(self, raw: int, max_score: int) -> int:
        if max_score == 0:
            return self.MIN_SCORE
        normalized = raw / max_score
        scaled = self.MIN_SCORE + normalized * (self.MAX_SCORE - self.MIN_SCORE)
        return round(scaled)