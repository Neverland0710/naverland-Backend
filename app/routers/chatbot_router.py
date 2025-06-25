from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chatbot_schema import ChatRequest
from app.chatbot.embedding import get_embedding_and_emotion
from app.chatbot.qdrant_service import search_similar_memories_with_emotion
from app.chatbot.gpt_service import generate_response
from app.dependencies.deps import get_db
from app.db.models.text_conversation_TB import TextConversationTB
from uuid import uuid4
from sqlalchemy.sql import func

router = APIRouter()

@router.post("/ask")
def ask_chatbot(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_question = request.question.strip()
        if not user_question:
            return {"error": "❌ 질문이 비어 있습니다."}

        # ✅ 1. 임베딩 + 감정 추론
        embedding, emotion = get_embedding_and_emotion(user_question)
        if not embedding or not emotion:
            return {"error": "❌ 임베딩 또는 감정 추론 실패"}

        # ✅ 2. 유사한 감정의 기억 검색
        similar_messages = search_similar_memories_with_emotion(embedding, emotion)
        if not similar_messages:
            return {"error": "❌ 감정 기반 유사 메시지를 찾을 수 없습니다."}

        # ✅ 3. GPT 응답 생성 (감정 포함)
        gpt_reply = generate_response(user_question, emotion, similar_messages)

        # ✅ 4. 질문 저장
        db.add(TextConversationTB(
            text_id=str(uuid4()),
            auth_key_id=str(request.auth_key_id),
            role=request.role,
            content=user_question,
            created_at=func.now()
        ))

        # ✅ 5. 챗봇 응답 저장
        db.add(TextConversationTB(
            text_id=str(uuid4()),
            auth_key_id=str(request.auth_key_id),
            role="chatbot",
            content=gpt_reply,
            created_at=func.now()
        ))

        db.commit()

        # ✅ 6. 응답 반환 (감정 포함)
        return {
            "answer": gpt_reply,
            "emotion": emotion,
            "context": similar_messages
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"🔥 서버 내부 오류: {str(e)}"}
