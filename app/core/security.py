from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from app.db.database import get_db
from app.db.models.user_TB import User
from sqlalchemy.orm import Session
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> User:
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid JWT payload")
    except JWTError:
        raise HTTPException(401, "Invalid JWT token")

    user = db.query(User).filter(User.USER_ID == user_id).first()
    if not user:
        raise HTTPException(401, "User not found")

    return user
