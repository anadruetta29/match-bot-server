from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class AnswerModel(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    question_id = Column(String)
    question_text = Column(Text)
    topic = Column(String)
    option_id = Column(Integer)
    option_text = Column(Text)
    score = Column(Integer)
    response_text = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionModel", back_populates="answers")


