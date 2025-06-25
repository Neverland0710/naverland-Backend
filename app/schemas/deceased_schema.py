from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional

# ✅ 고인 등록 요청용
class DeceasedCreate(BaseModel):
    name: str
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    image_path: Optional[str] = None
    relation_in_family: Optional[str] = None

# ✅ 고인 정보 응답용
class DeceasedResponse(DeceasedCreate):
    deceased_id: UUID
    registered_at: datetime

    class Config:
        orm_mode = True
