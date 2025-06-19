from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_TB, auth, me           # me: 보호 API 예시
from app.db.database import Base, engine

import logging

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ✅ 요청 로그 출력용 미들웨어 추가
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn.access")
    logger.info(f"📥 Request: {request.method} {request.url}")
    
    # POST, PUT 요청의 바디 출력
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.body()
            logger.info(f"📦 Body: {body.decode('utf-8')}")
        except Exception as e:
            logger.warning(f"⚠️ Could not parse body: {e}")

    logger.info(f"📄 Headers: {dict(request.headers)}")

    response = await call_next(request)
    return response

# 라우터 등록
app.include_router(user_TB.router)
app.include_router(auth.router)
app.include_router(me.router)

@app.get("/")
def root():
    return {"message": "FastAPI + MySQL 연동 성공!"}
