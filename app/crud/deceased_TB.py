from sqlalchemy.orm import Session
from uuid import uuid4
from app.db.models.deceased_TB import DeceasedTB
from app.schemas.deceased_schema import DeceasedCreate

# ✅ 고인 정보 등록
def create_deceased(db: Session, deceased: DeceasedCreate) -> DeceasedTB:
    db_deceased = DeceasedTB(
        deceased_id=str(uuid4()),
        name=deceased.name,
        birth_date=deceased.birth_date,
        death_date=deceased.death_date,
        image_path=deceased.image_path,
        relation_in_family=deceased.relation_in_family,
    )
    db.add(db_deceased)
    db.commit()
    db.refresh(db_deceased)
    return db_deceased

# ✅ 고인 ID로 조회
def get_deceased_by_id(db: Session, deceased_id: str) -> DeceasedTB:
    return db.query(DeceasedTB).filter(DeceasedTB.deceased_id == deceased_id).first()
