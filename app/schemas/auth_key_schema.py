from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# ✅ 인증키 생성 요청용
class AuthKeyCreate(BaseModel):
    user_id: UUID
    deceased_id: UUID

# ✅ 인증키 정보 응답용
class AuthKeyResponse(AuthKeyCreate):
    auth_key_id: UUID
    is_valid: bool
    issued_at: datetime
    expired_at: Optional[datetime] = None

    class Config:
        orm_mode = True
