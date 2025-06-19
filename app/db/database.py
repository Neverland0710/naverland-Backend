"""
app/db/database.py
────────────────────────────────────────────────────────
SQLAlchemy + MySQL 세션·엔진 설정 모듈
.env 파일의 DB_* 변수만 바꾸면 다른 DB로도 쉽게 전환 가능
────────────────────────────────────────────────────────
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# 1) .env 환경 변수 로드
load_dotenv()

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT")
DB_NAME     = os.getenv("DB_NAME")

# 2) 접속 URL(utf8mb4 + pool_recycle)
DB_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# 3) Engine & Session 설정
engine = create_engine(
    DB_URL,
    echo=True,          # 개발 중 쿼리 로그 출력 / 운영 시 False 권장
    pool_recycle=3600   # MySQL 연결 끊김 방지
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# 4) Base 클래스 (모델들이 이걸 상속)
Base = declarative_base()

# 5) FastAPI Depends용 DB 세션 함수
def get_db():
    """
    라우터에서: 
        db: Session = Depends(get_db)
    로 주입하여 세션을 안전하게 관리
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
