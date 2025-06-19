# Python 이미지 기반
FROM python:3.13.4

# 작업 디렉토리 생성
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
RUN pip install firebase-admin
RUN pip install -r requirements.txt