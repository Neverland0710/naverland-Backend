from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.db.models.auth_key_TB import AuthKeyTB
from app.schemas.auth_key_schema import AuthKeyCreate

# ✅ 사용자와 고인 간 인증키 발급
def create_auth_key(db: Session, data: AuthKeyCreate) -> AuthKeyTB:
    db_key = AuthKeyTB(
        auth_key_id=str(uuid4()),
        user_id=str(data.user_id),
        deceased_id=str(data.deceased_id),
        issued_at=datetime.utcnow()
    )
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key

# ✅ 인증키 ID로 조회
def get_auth_key_by_id(db: Session, auth_key_id: str) -> AuthKeyTB:
    return db.query(AuthKeyTB).filter(AuthKeyTB.auth_key_id == auth_key_id).first()
