FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN set -eux; \
    apt-get update -o Acquire::Retries=3; \
    apt-get install -y --no-install-recommends xvfb xauth; \
    playwright install-deps; \
    playwright install; \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p allure-results logs
