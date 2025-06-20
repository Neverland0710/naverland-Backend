from fastapi import APIRouter
from app.schemas.chatbot_schema import ChatRequest
from app.chatbot.embedding import get_embedding
from app.chatbot.qdrant_service import search_similar_memories
from app.chatbot.gpt_service import generate_response

router = APIRouter()

@router.post("/ask")
def ask_chatbot(request: ChatRequest):
    try:
        user_question = request.question
        query_vector = get_embedding(user_question)

        if not query_vector:
            return {"error": "❌ 임베딩 실패"}

        similar_messages = search_similar_memories(query_vector)

        if not similar_messages:
            return {"error": "❌ 유사 메시지 없음"}

        gpt_reply = generate_response(user_question, similar_messages)

        return {"answer": gpt_reply, "context": similar_messages}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"🔥 서버 내부 오류: {str(e)}"}
