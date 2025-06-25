# app/models/deceased_TB.py

from sqlalchemy import Column, String, Date, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import CHAR
from uuid import uuid4

from app.db.database import Base

class DeceasedTB(Base):
    __tablename__ = "deceased_TB"

    deceased_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    death_date = Column(Date)
    image_path = Column(Text)  # 고인 이미지 경로
    registered_at = Column(DateTime, default=func.now())
    relation_in_family = Column(String(100))  # 예: 엄마, 아빠, 할머니
