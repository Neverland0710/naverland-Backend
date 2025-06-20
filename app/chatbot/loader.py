# app/chatbot/setup_memories.py

import json
import os
from app.chatbot.embedding import get_embedding
from app.chatbot.qdrant_service import create_collection, upload_memory

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mother_dauther.json")

def load_initial_memories():
    create_collection()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"📦 총 {len(data)}개의 메시지 로드 중...")

    for item in data:
        message = item.get("text")
        sender = item.get("speaker")
        if not message or not sender:
            continue

        embedding = get_embedding(message)
        if embedding:
            upload_memory(
                text=message,
                embedding=embedding,
                metadata={"speaker": sender.lower()}
            )

    print("✅ 초기 대화 메시지 벡터 저장 완료.")

if __name__ == "__main__":
    load_initial_memories()
