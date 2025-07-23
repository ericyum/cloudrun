# Python 3.9-slim 이미지를 기반으로 합니다.
FROM python:3.9-slim

# 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# requirements.txt를 복사하고 라이브러리를 설치합니다.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 소스 코드를 복사합니다.
COPY . .

# Gunicorn을 사용하여 애플리케이션을 실행합니다.
# Cloud Run은 PORT 환경 변수를 통해 포트를 동적으로 주입합니다.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
