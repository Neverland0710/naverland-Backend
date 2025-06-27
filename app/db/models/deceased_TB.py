# app/models/deceased_TB.py

from sqlalchemy import Column, String, Date, DateTime, Text,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from uuid import uuid4

from app.db.database import Base

class DeceasedTB(Base):
    __tablename__ = "deceased_TB"

    deceased_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    death_date = Column(Date)
    image_path = Column(Text)  # 고인 이미지 경로
    speaking_style = Column(Text(50))
    nickname = Column(String(50), nullable=False)
    personality = Column(Text)
    hobbies = Column(Text)
    registered_at = Column(DateTime, default=func.now())
    creator_user_id = Column(String(36), ForeignKey("user_TB.user_id"), nullable=False)
