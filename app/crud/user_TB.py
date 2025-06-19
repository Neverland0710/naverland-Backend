from sqlalchemy.orm import Session
from app.db.models.user_TB import User
from app.schemas.user_TB import UserCreate
from typing import Optional
from uuid import uuid4

# ✅ 신규 사용자 생성 함수 (UUID 자동 생성 포함)
def create_user(db: Session, user: UserCreate) -> User:
    """
    새 사용자 정보를 DB에 저장한다.
    - UUID는 프론트에서 안 넘겨준 경우 자동 생성
    - 소셜 로그인 시 비밀번호는 None 가능
    """
    user_data = user.dict()

    # UUID 없을 경우 자동 생성
    if not user_data.get("USER_ID"):
        user_data["USER_ID"] = str(uuid4())

    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ 이메일로 사용자 조회 (로그인 중복 방지용)
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    이메일로 기존 사용자 조회
    - 구글 로그인 또는 회원가입 시 중복 방지용
    """
    return db.query(User).filter(User.EMAIL == email).first()

# ✅ USER_ID로 단일 사용자 조회
def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    사용자 ID로 단일 사용자 조회
    """
    return db.query(User).filter(User.USER_ID == user_id).first()

# ✅ 전체 사용자 목록 조회 (관리자용/디버깅용)
def get_all_users(db: Session) -> list[User]:
    """
    전체 사용자 목록 반환
    """
    return db.query(User).all()
