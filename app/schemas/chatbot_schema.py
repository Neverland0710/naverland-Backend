from pydantic import BaseModel
from uuid import UUID
from typing import Literal, Optional
from datetime import datetime

# ✅ 챗봇 요청용 스키마
class ChatRequest(BaseModel):
    auth_key_id: UUID                         # 인증키 (사용자 식별)
    role: Literal["user", "chatbot"] = "user" # 메시지 주체 (기본값: user)
    question: str                             # 실제 질문 내용

# ✅ DB에 저장된 대화 응답 반환용 (Optional)
class ChatResponse(BaseModel):
    text_id: UUID
    auth_key_id: UUID
    role: Literal["user", "chatbot"]
    content: str
    emotion: Optional[str] = None             # ✅ 감정 필드 (응답 시 포함 가능)
    created_at: datetime

    class Config:
        orm_mode = True
