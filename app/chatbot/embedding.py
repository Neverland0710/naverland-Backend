# app/chatbot/embedding.py

import openai
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "text-embedding-3-small"  # ✅ 차원: 1536

def get_embedding(text: str) -> List[float]:
    try:
        response = openai.embeddings.create(
            model=MODEL_NAME,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ 임베딩 실패: {e}")
        return []
