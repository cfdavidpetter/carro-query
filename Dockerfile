FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    bash \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000

# CMD ["python", "-m", "alembic", "upgrade", "head"]

