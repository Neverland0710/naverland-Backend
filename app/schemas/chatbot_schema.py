from pydantic import BaseModel

# ✅ 챗봇 요청용 스키마
class ChatRequest(BaseModel):
    question: str          # 사용자가 입력한 질문
    user_id: str           # 어떤 유족(또는 테스트 계정)인지 구분