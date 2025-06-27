from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from sqlalchemy.sql import func
from starlette.concurrency import run_in_threadpool  # ✅ 중요

from app.schemas.chatbot_schema import ChatRequest
from app.chatbot.embedding import get_embedding
from app.chatbot.qdrant_service import search_similar_memories
from app.chatbot.gpt_service import generate_response
from app.dependencies.deps import get_db
from app.db.models.text_conversation_TB import TextConversationTB

router = APIRouter()

@router.post("/ask")
async def ask_chatbot(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_question = request.question.strip()
        if not user_question:
            return {"error": "❌ 질문이 비어 있습니다."}

        # ✅ 1. 질문 임베딩
        embedding = get_embedding(user_question)
        if not embedding:
            return {"error": "❌ 임베딩 실패"}

        # ✅ 2. user_id 기준 벡터 검색
        similar_messages = search_similar_memories(
            query_vector=embedding,
            user_id=request.user_id,
            top_k=5
        )
        if not similar_messages:
            return {"error": "❌ 유사 메시지를 찾을 수 없습니다."}

        # ✅ 3. GPT 응답 생성 (동기 함수 -> 비동기 안전 실행)
        gpt_reply = await run_in_threadpool(
            generate_response,
            request.user_id,
            user_question
            )

        # ✅ 로그 (선택)
        print("📥 질문:", user_question)
        print("📎 유사 문맥 수:", len(similar_messages))
        print("🤖 GPT 응답:", gpt_reply)

        # ✅ 4. 응답 반환
        return {
            "answer": gpt_reply,
            "context": similar_messages
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"🔥 서버 내부 오류: {str(e)}"}
