import uuid

_sessions = {}

class SessionService:

    @staticmethod
    def get_or_create(session_id: str | None):
        if session_id and session_id in _sessions:
            return session_id, _sessions[session_id]

        new_id = str(uuid.uuid4())
        _sessions[new_id] = {
            "answers": [],
            "step": 0
        }
        return new_id, _sessions[new_id]