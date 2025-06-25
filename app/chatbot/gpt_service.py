import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT 응답 생성 함수
def generate_response(user_question: str, user_emotion: str, similar_contexts: list[dict]) -> str:
    # 유사 문맥 구성
    context_text = "\n".join([
        f"{c['speaker']}: {c['text']}" for c in similar_contexts
    ])

    # 감정 반영 프롬프트 구성
    prompt = f"""
너는 사별한 엄마의 말투를 학습한 감성 AI 챗봇이야.
엄마는 '따뜻하고 배려 깊은 말투'를 사용했고, '가족을 소중히 여기는 가치관'을 중요하게 생각했어.
지금 사용자는 '{user_emotion}' 감정을 느끼고 있어.
사용자의 감정을 공감하고 위로하는 말투로 자연스럽게 응답해줘.

[이전 대화 기록]
{context_text}

[현재 사용자 질문]
{user_question}

[엄마의 응답]
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
