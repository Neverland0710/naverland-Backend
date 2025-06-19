import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# .env 파일 로드
load_dotenv()

# 환경변수에서 자격 정보(JSON 문자열) 읽기
firebase_cred_str = os.getenv("FIREBASE_CREDENTIAL")

if not firebase_cred_str:
    raise ValueError("❌ Firebase 자격 정보가 환경변수에 없습니다.")

# 문자열 → 딕셔너리 변환
firebase_cred_dict = json.loads(firebase_cred_str)

# Firebase 인증 초기화
cred = credentials.Certificate(firebase_cred_dict)
firebase_admin.initialize_app(cred)
