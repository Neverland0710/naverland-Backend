import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, initialize_app

# ✅ 환경변수 로드
load_dotenv()
path = os.getenv("FIREBASE_CREDENTIAL_PATH")

if not path:
    raise RuntimeError("❌ Firebase 경로가 비어있음")

cred = credentials.Certificate(path)

# ✅ Firebase 초기화
if not firebase_admin._apps:
    initialize_app(cred)
    print("✅ Firebase 초기화 완료")
else:
    print("ℹ️ 이미 Firebase 초기화됨")
