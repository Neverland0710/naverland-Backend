from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user
from app.db.models.user_TB import User
from app.schemas.user_TB import UserResponse

router = APIRouter(prefix="/me", tags=["auth"])

@router.get("/", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
