# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

# ✅ DB 설정
from app.db.database import Base, engine
Base.metadata.create_all(bind=engine)

# ✅ 라우터 import
from app.routers.user_TB import router as user_router
from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.routers.chatbot_router import router as chatbot_router  # ✅ 정확한 방식
from app.routers.deceased_router import router as deceased_router
from app.routers.auth_key_router import router as auth_key_router
# ✅ FastAPI 앱 생성
app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ✅ 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chatbot")  # uvicorn.access 사용 지양

# ✅ 요청 로그 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 Request: {request.method} {request.url}")
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.body()
            logger.info(f"📦 Body: {body.decode('utf-8')}")
        except Exception as e:
            logger.warning(f"⚠️ Could not parse body: {str(e)}")
    logger.info(f"📄 Headers: {dict(request.headers)}")
    return await call_next(request)


# ✅ 라우터 등록
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
app.include_router(me_router, prefix="/me")
app.include_router(chatbot_router, prefix="/chatbot")  # ✅ 챗봇 API 라우터
app.include_router(deceased_router, prefix="/deceased")
app.include_router(auth_key_router, prefix="/auth-key")
# ✅ 기본 루트 엔드포인트
@app.get("/")
def root():
    return {"message": "✅ FastAPI + MySQL 서버 정상 작동 중!"}

# ✅ 등록된 경로 확인용 디버깅 (선택)
@app.on_event("startup")
def debug_routes():
    for route in app.routes:
        print(f"✅ 등록된 경로: {route.path} - {route.name}")
