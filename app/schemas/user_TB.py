from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ✅ 사용자 생성용 입력 모델
class UserCreate(BaseModel):
    USER_ID: str                           # 프론트에서 UUID 생성하거나 백엔드에서 UUID 자동 부여
    NAME: str                              # 사용자 이름 또는 닉네임
    PASSWORD: Optional[str] = None         # 소셜 로그인은 None 가능
    EMAIL: EmailStr                        # 고유 이메일 주소 (구글 계정 등)
    RELATION_TO_DECEASED: Optional[str] = None  # 고인과의 관계 (예: 딸, 아들 등)

# ✅ 사용자 조회 응답 모델
class UserResponse(BaseModel):
    USER_ID: str
    NAME: str
    EMAIL: EmailStr
    JOINED_AT: datetime
    RELATION_TO_DECEASED: Optional[str]

    class Config:
        from_attributes = True  # SQLAlchemy 모델과의 호환성을 위해 설정

