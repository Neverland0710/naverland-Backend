import os
import json
from dotenv import load_dotenv
from .embedding import get_embedding  # ✅ text-embedding-3-small 사용
from app.chatbot.qdrant_service import create_collection, upload_memory

load_dotenv()

# ✅ (파일 경로, 유저 ID) 튜플로 구성
FILES = [
    (os.path.join(os.path.dirname(__file__), "..", "data", "유학간 딸.json"), "user_mother_daughter"),
    (os.path.join(os.path.dirname(__file__), "..", "data", "출장.json"), "user_husband_wife"),
    (os.path.join(os.path.dirname(__file__), "..", "data", "출장아빠_딸.json"), "user_father_daughter"),
]

def load_and_upload():
    create_collection()  # ✅ 컬렉션 초기화 (벡터 차원 1536 고정)

    total_uploaded = 0

    for file_path, user_id in FILES:
        with open(file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)

        for item in messages:
            message = item.get("message")
            sender = item.get("sender")

            if not message or not sender:
                continue

            embedding = get_embedding(message)
            if not embedding:
                continue

            upload_memory(
                text=message,
                embedding=embedding,
                metadata={
                    "user_id": user_id,
                    "speaker": sender.lower(),
                    "page_content": message,
                }
            )
            total_uploaded += 1

    print(f"✅ Qdrant 업로드 완료: 총 {total_uploaded}개 메시지")

if __name__ == "__main__":
    load_and_upload()
