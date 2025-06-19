from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
import os
from dotenv import load_dotenv

# DB 관련
from app.dependencies.deps import get_db
from app.schemas.user_TB import UserCreate
from app.crud import user_TB as crud_user

# 환경변수 로드
load_dotenv()

# ✅ 환경변수 또는 직접 지정
SECRET_KEY = os.getenv("SECRET_KEY", "test-dev-secret-key")
ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")  # 여기에 실제 Web Client ID 넣기

router = APIRouter(prefix="/auth", tags=["auth"])

# 📥 요청 스키마
class SocialLoginRequest(BaseModel):
    provider: str
    access_token: str

# 📤 응답 스키마
class SocialLoginResponse(BaseModel):
    id: str
    email: str
    name: str
    provider: str
    access_token: str  # JWT

# ✅ Google ID Token 검증 함수
def verify_google_token(id_token_str: str) -> dict:
    try:
        print("🔍 받은 ID 토큰 일부:", id_token_str[:30])
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )
        print("✅ 검증 성공:", idinfo)
        return {
            "email": idinfo["email"],
            "name": idinfo.get("name", "NoName")
        }
    except Exception as e:
        print("❌ Token verification failed:", e)
        raise HTTPException(status_code=401, detail="Invalid Google ID token")

# 🎯 실제 로그인 엔드포인트
@router.post("/social-login", response_model=SocialLoginResponse)
async def social_login(data: SocialLoginRequest, db: Session = Depends(get_db)):
    if data.provider != "google":
        raise HTTPException(status_code=400, detail="Unsupported provider")

    # 1. 토큰 검증
    user_info = verify_google_token(data.access_token)

    # 2. 유저 DB에 있는지 확인
    user = crud_user.get_user_by_email(db, user_info["email"])
    if not user:
        new_user = UserCreate(
            USER_ID=str(uuid4()),
            EMAIL=user_info["email"],
            NAME=user_info["name"],
            PASSWORD=None,
            PROVIDER="google"
        )
        user = crud_user.create_user(db, new_user)

    # 3. JWT 발급
    token = jwt.encode({"sub": str(user.USER_ID)}, SECRET_KEY, algorithm=ALGORITHM)

    # 4. 응답 반환
    return SocialLoginResponse(
        id=str(user.USER_ID),
        email=user.EMAIL,
        name=user.NAME,
        provider="google",
        access_token=token
    )