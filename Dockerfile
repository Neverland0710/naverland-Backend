# ✅ Python 베이스 이미지
FROM python:3.13.4

# ✅ 작업 디렉토리 설정
WORKDIR /app

# ✅ 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 애플리케이션 소스 복사
COPY . .

# ✅ 컨테이너 포트 오픈
EXPOSE 8000

# ✅ FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
