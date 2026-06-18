from sqlalchemy import Column, Integer, String,Text
from app.db import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    cv_name = Column(String,nullable=False)
    offer_name = Column(String, nullable=False)
    candidate_skills = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    decision = Column(String, nullable=False)