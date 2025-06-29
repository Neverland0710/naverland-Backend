from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4
from jose import jwt
import os
from dotenv import load_dotenv

# 🔌 Firebase Admin
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

# 🔌 내부 종속
from app.dependencies.deps import get_db
from app.schemas.user_TB import UserCreate
from app.crud import user_TB as crud_user

# 🔄 .env 불러오기
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "test-dev-secret-key")
ALGORITHM = "HS256"

# ✅ Firebase 초기화 (경로 기반)
firebase_path = os.getenv("FIREBASE_CREDENTIAL_PATH")
if not firebase_path:
    raise RuntimeError("❌ 환경변수 FIREBASE_CREDENTIAL_PATH가 비어 있습니다.")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_path)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase 초기화 완료")
    except Exception as e:
        raise RuntimeError(f"❌ Firebase 초기화 실패: {e}")

# 🔧 라우터 설정
router = APIRouter(tags=["auth"])

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
    access_token: str

# ✅ Firebase Token 검증
def verify_firebase_token(id_token_str: str):
    try:
        decoded_token = firebase_auth.verify_id_token(id_token_str)
        print("✅ Firebase Token 검증 성공:", decoded_token)
        return {
            "email": decoded_token["email"],
            "name": decoded_token.get("name", "NoName"),
            "uid": decoded_token["uid"]
        }
    except Exception as e:
        print("❌ Firebase Token 검증 실패:", e)
        raise HTTPException(status_code=401, detail=f"Invalid Firebase ID token: {str(e)}")

# ✅ 소셜 로그인 엔드포인트
@router.post("/social-login", response_model=SocialLoginResponse)
async def social_login(data: SocialLoginRequest, db: Session = Depends(get_db)):
    if data.provider.lower() != "google":
        raise HTTPException(status_code=400, detail="Unsupported provider")

    user_info = verify_firebase_token(data.access_token)

    # 유저가 DB에 없으면 새로 생성
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

    token = jwt.encode({"sub": str(user.USER_ID)}, SECRET_KEY, algorithm=ALGORITHM)

    return SocialLoginResponse(
        id=str(user.USER_ID),
        email=user.EMAIL,
        name=user.NAME,
        provider="google",
        access_token=token
    )
