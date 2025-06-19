# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_TB import router as user_router
from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.db.database import Base, engine
import logging

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# 요청 로그 미들웨어
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn.access")
    logger.info(f"📥 Request: {request.method} {request.url}")
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.body()
            logger.info(f"📦 Body: {body.decode('utf-8')}")
        except Exception as e:
            logger.warning(f"⚠️ Could not parse body: {e}")
    logger.info(f"📄 Headers: {dict(request.headers)}")
    return await call_next(request)

# 라우터 등록 (prefix는 여기서만!)
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
app.include_router(me_router, prefix="/me")

@app.get("/")
def root():
    return {"message": "✅ FastAPI + MySQL 서버 정상 작동 중!"}
