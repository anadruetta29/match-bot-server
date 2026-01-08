from sqlalchemy import Column, String, DateTime, Integer, JSON, Boolean
from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from app.database.session import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    finished_at = Column(DateTime, nullable=True)
    total_score = Column(Integer, nullable=True)
    features = Column(JSON, nullable=True)
    user_feedback = Column(Boolean, nullable=True)

    answers = relationship("AnswerModel", back_populates="session")
