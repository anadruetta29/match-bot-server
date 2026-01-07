from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("AnswerModel", back_populates="session")
