from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.deceased_schema import DeceasedCreate, DeceasedResponse
from app.crud import deceased_TB as crud
from app.dependencies.deps import get_db

router = APIRouter( tags=["Deceased"])

# ✅ 고인 정보 등록 API
@router.post("/", response_model=DeceasedResponse)
def register_deceased(data: DeceasedCreate, db: Session = Depends(get_db)):
    return crud.create_deceased(db, data)

# ✅ 고인 ID로 정보 조회 API
@router.get("/{deceased_id}", response_model=DeceasedResponse)
def get_deceased(deceased_id: str, db: Session = Depends(get_db)):
    result = crud.get_deceased_by_id(db, deceased_id)
    if not result:
        raise HTTPException(404, detail="고인 정보를 찾을 수 없습니다.")
    return result

