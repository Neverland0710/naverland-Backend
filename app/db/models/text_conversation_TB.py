from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.database import Base  # ⬅️ Base는 너의 SQLAlchemy 세팅에 맞게 수정 필요

class TextConversationTB(Base):
    __tablename__ = "text_conversation_TB"

    text_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    auth_key_id = Column(CHAR(36), ForeignKey("auth_key_TB.auth_key_id"), nullable=False)
    role = Column(String(10), nullable=False)  # 'user' 또는 'chatbot'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
