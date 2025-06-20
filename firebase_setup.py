from firebase_admin import credentials, initialize_app
import os
from dotenv import load_dotenv

load_dotenv()  # .env에서 경로 읽기
path = os.getenv("FIREBASE_CREDENTIAL_PATH")

if not path:
    raise RuntimeError("❌ Firebase 경로가 비어있음")

cred = credentials.Certificate(path)

if not firebase_admin._apps:
    initialize_app(cred)
    print("✅ Firebase 초기화 완료")
else:
    print("ℹ️ 이미 Firebase 초기화됨")
