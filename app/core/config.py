# app/core/config.py

import os
from dotenv import load_dotenv

# 🔄 .env 파일 로드
load_dotenv()

class Settings:
    # 🔐 DB 접속 정보
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # 🌐 서버 고정 IP 주소
    BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")

    # 🔐 Google OAuth 및 보안 설정
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")

# ✅ settings 인스턴스 생성
settings = Settings()
