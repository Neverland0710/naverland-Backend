import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_input: str, memories: list) -> str:
    """
    GPT에게 고인의 메시지 기반으로 감성적인 응답 생성 요청
    """
    context_text = "\n".join(
        [f"{i+1}. {m['text']}" for i, m in enumerate(memories)]
    )

    prompt = f"""
다음은 고인이 생전에 보낸 메시지입니다:
{context_text}

위 내용을 참고해서 아래 질문에 대해 고인의 말투로 따뜻하게 위로해 주세요.

질문: "{user_input}"
응답:
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
