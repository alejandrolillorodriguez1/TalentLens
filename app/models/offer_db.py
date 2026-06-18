from sqlalchemy import Column, Integer, String,Text
from app.db import Base

class JobOffer(Base):
    __tablename__ = "offer_job"

    id = Column(Integer, primary_key=True, index=True)
    offer_name = Column(String,nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False)
