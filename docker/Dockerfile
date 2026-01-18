FROM python:3.10-slim

# 環境変数
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリ
WORKDIR /app

# システムパッケージインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージインストール
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ポート公開
EXPOSE 8000
