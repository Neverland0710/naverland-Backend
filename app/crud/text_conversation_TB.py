from sqlalchemy.orm import Session
from uuid import uuid4
from sqlalchemy.sql import func

from app.db.models.text_conversation_TB import TextConversationTB
from app.schemas.chatbot_schema import ChatRequest

# ✅ 사용자 메시지 또는 챗봇 응답 저장
def save_message(db: Session, request: ChatRequest, content: str):
    message = TextConversationTB(
        text_id=str(uuid4()),
        auth_key_id=str(request.auth_key_id),
        role=request.role,
        content=content,
        created_at=func.now()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# ✅ 전체 대화 불러오기 (선택 기능)
def get_messages_by_auth_key(db: Session, auth_key_id: str):
    return db.query(TextConversationTB)\
             .filter(TextConversationTB.auth_key_id == auth_key_id)\
             .order_by(TextConversationTB.created_at.asc())\
             .all()
