from app.chatbot.qdrant_service import search_similar_memories
from app.chatbot.embedding import get_embedding
from openai import OpenAI
import os
from dotenv import load_dotenv

# ✅ .env에서 OpenAI API 키 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ GPT 응답 생성 함수
def generate_response(user_question: str, similar_contexts: list[dict]) -> str:
    context_text = "\n".join([
        f"{c.get('metadata', {}).get('speaker', '고인')}: {c.get('text', '')}" for c in similar_contexts
    ])

    prompt = f"""
너는 고인이 된 엄마의 말투를 학습한 감성 AI 챗봇이야.
엄마는 따뜻하고 다정한 말투로, 딸과의 대화를 소중히 여겼어.
지금 사용자가 엄마에게 말을 걸고 있어.
과거의 대화 기록을 참고해서 엄마처럼 자연스럽게 응답해줘.

[이전 대화 기록]
{context_text}

[현재 사용자 질문]
{user_question}

[엄마의 응답]
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=512
    )

    return response.choices[0].message.content.strip()

# ✅ 테스트 실행 파트
if __name__ == "__main__":
    query = input("💬 사용자 질문: ").strip()
    if not query:
        print("❗ 질문이 비어있습니다.")
        exit()

    # ✅ 사용자 ID (하드코딩된 테스트용)
    user_id = "user_mother_daughter"

    # ✅ 임베딩 + 유사 메시지 검색
    embedding = get_embedding(query)
    results = search_similar_memories(embedding, user_id)


    # ✅ 유사 메시지 출력
    print("\n🔍 유사 메시지:")
    for res in results:
        print(f"- {res['metadata']['speaker']}: {res['text']} (score: {res['score']:.4f})")

    # ✅ GPT 응답 생성
    response = generate_response(query, results)

    # ✅ 최종 응답 출력
    print("\n🤖 GPT 응답:")
    print(response)
