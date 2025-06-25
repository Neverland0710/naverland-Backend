# app/models/auth_key_TB.py

from sqlalchemy import Column, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.database import Base

class AuthKeyTB(Base):
    __tablename__ = "auth_key_TB"

    auth_key_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(CHAR(36), ForeignKey("user_TB.user_id"), nullable=False)
    deceased_id = Column(CHAR(36), ForeignKey("deceased_TB.deceased_id"), nullable=False)

    is_valid = Column(Boolean, default=True)
    issued_at = Column(DateTime, default=func.now())
    expired_at = Column(DateTime, nullable=True)

