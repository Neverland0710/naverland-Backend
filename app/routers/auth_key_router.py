from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth_key_schema import AuthKeyCreate, AuthKeyResponse
from app.crud import auth_key_TB as crud
from app.dependencies.deps import get_db

router = APIRouter( tags=["AuthKey"])

# ✅ 인증키 발급 API
@router.post("/", response_model=AuthKeyResponse)
def issue_auth_key(data: AuthKeyCreate, db: Session = Depends(get_db)):
    return crud.create_auth_key(db, data)

# ✅ 인증키 ID로 인증 정보 조회 API
@router.get("/{auth_key_id}", response_model=AuthKeyResponse)
def get_auth_key(auth_key_id: str, db: Session = Depends(get_db)):
    result = crud.get_auth_key_by_id(db, auth_key_id)
    if not result:
        raise HTTPException(404, detail="인증키 정보를 찾을 수 없습니다.")
    return result

