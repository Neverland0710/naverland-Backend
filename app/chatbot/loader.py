import json
import os
from app.chatbot.qdrant_service import create_collection, upload_memory

# ✅ 상대 경로 기준 데이터 위치
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "최종_임베딩포함.json")

def load_precomputed_memories():
    create_collection()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"📦 총 {len(data)}개의 메시지 로드 중...")

    for item in data:
        message = item.get("message")
        speaker = item.get("sender")
        embedding = item.get("embedding")
        emotion = item.get("emotion")

        if not message or not speaker or not embedding or not emotion:
            print(f"⚠️ 필수 정보 누락 → 건너뜀: {message}")
            continue

        upload_memory(
            text=message,
            embedding=embedding,
            metadata={
                "speaker": speaker.lower(),
                "emotion": emotion,
                "page_content": message  # ✅ RAG에서 필요함
    }
)

    print("✅ 미리 계산된 메시지 벡터 저장 완료.")

# ✅ -m으로 실행 가능하도록 진입점 설정
if __name__ == "__main__":
    load_precomputed_memories()
