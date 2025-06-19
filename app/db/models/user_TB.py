from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "user_TB"

    # 사용자 고유 ID (UUID 문자열)
    USER_ID = Column(String(36), primary_key=True)

    # 사용자 이름 또는 닉네임 (필수)
    NAME = Column(String(100), nullable=False)

    # 비밀번호 (소셜 로그인은 NULL 가능)
    PASSWORD = Column(String(255), nullable=True)

    # 이메일 (필수 + 유일)
    EMAIL = Column(String(100), unique=True, nullable=False)

    # 가입일시 (기본값: 현재 시각)
    JOINED_AT = Column(DateTime, default=datetime.utcnow)

    # 고인과의 관계 (예: 엄마, 아빠 등)
    RELATION_TO_DECEASED = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<User(USER_ID='{self.USER_ID}', EMAIL='{self.EMAIL}', NAME='{self.NAME}')>"
