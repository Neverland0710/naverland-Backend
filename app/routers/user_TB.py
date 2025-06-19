# 🔽 기존 코드 유지
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.deps import get_db
from app.schemas.user_TB import UserCreate, UserResponse
from app.crud import user_TB as crud_user

# 🔽 Google Token 검증용 추가
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter(prefix="/users", tags=["users"])

# ✅ 기존 API
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)

# ✅ 추가: ID 토큰 검증 엔드포인트
class TokenRequest(BaseModel):
    id_token: str

@router.post("/verify")
def verify_token(token_request: TokenRequest):
    try:
        CLIENT_ID = "518285855054-rjtgih49d2jh6uvf71j7g91339cs9n0v.apps.googleusercontent.com"  # ← 실제 클라이언트 ID로 교체

        decoded_token = id_token.verify_oauth2_token(
            token_request.id_token,
            requests.Request(),
            CLIENT_ID,
        )

        return {
            "email": decoded_token.get("email"),
            "uid": decoded_token.get("sub"),   # 또는 "user_id"
            "name": decoded_token.get("name"),
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
