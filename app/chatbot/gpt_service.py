# ✅ gpt_service.py (LangChain + Runnable 기반으로 전환)

import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

from chatbot.embedding import get_embedding
from chatbot.qdrant_service import search_similar_memories

load_dotenv()

# ✅ GPT 모델 초기화
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)


# ✅ 프롬프트 템플릿
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 감성 AI 추모 챗봇이야. 고인의 말투를 재현해서 유족에게 따뜻하게 응답해줘."),   
    ("placeholder", "{chat_history}"),
    ("user", "{input}")
])

# ✅ Runnable Chain + 세션별 히스토리 관리
chat_chain = RunnableWithMessageHistory(
    prompt | llm,
    lambda session_id: InMemoryChatMessageHistory(),
    input_messages_key="input",
    history_messages_key="chat_history"
).with_config({"run_name": "chat-runnable"})

# ✅ 응답 생성 함수

def generate_response(user_id: str, user_question: str) -> str:
    try:
        # 1. 임베딩
        query_vector = get_embedding(user_question)
        if not query_vector:
            return "⚠️ 질문을 처리하는 데 문제가 생겼어요. 다시 시도해 주세요."

        # 2. 유사 문맥 검색
        similar_contexts = search_similar_memories(query_vector, user_id)

        # 3. 문맥 붙이기
        context_lines = [
            f"{c['metadata'].get('speaker', '고인')}: {c['text']}" for c in similar_contexts
        ]
        context = "\n".join(context_lines)
        combined_input = f"{context}\n\n{user_question}" if context else user_question

        # 4. RunnableWithMessageHistory 실행
        result = chat_chain.invoke(
            {"input": combined_input},
            config={"configurable": {"session_id": user_id}}
        )

        # 5. 응답 반환
        return result["output"].strip()

    except Exception as e:
        import traceback
        print("❌ GPT 호출 실패:", e)
        traceback.print_exc()
        return "⚠️ 대답을 준비하지 못했어요. 잠시 후 다시 시도해 주세요."

# ✅ 예시 실행용 (개발 중 테스트)
if __name__ == "__main__":
    answer = generate_response(
        user_id="user_mother_daughter",
        user_question="강릉 갔던거 기억나?"
    )
    print("💬 응답:", answer)
