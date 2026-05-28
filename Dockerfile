FROM python:3.11-slim-bookworm

ARG SERVER=http://host.docker.internal:8111/app/rest/
ARG UI_BASE_URL=http://host.docker.internal:8111

ENV SERVER=${SERVER}
ENV UI_BASE_URL=${UI_BASE_URL}
ENV PLAYWRIGHT_TEST_BASE_URL=${UI_BASE_URL}
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

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY . .

RUN mkdir -p allure-results logs

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["sh", "-c", "xvfb-run -a pytest -v --tb=short --alluredir allure-results"]