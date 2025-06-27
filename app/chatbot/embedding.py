from typing import List
import os
import openai
from dotenv import load_dotenv

# ✅ 환경변수 로드 (.env에 OPENAI_API_KEY 포함 필요)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ 임베딩 함수
def get_embedding(text: str) -> List[float]:
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        embedding = response.data[0].embedding
        if len(embedding) != 1536:
            raise ValueError(f"❌ 임베딩 벡터 차원 오류: {len(embedding)}")
        return embedding
    except Exception as e:
        print(f"❌ 임베딩 실패: {e}")
        return []

