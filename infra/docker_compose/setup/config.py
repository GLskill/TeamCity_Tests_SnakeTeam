import os

TC_URL = os.environ.get("UI_BASE_URL", "http://webapp:8111")
ENV_FILE = os.environ.get("ENV_FILE", "/app/.env")
TC_LOG = os.environ.get("TC_LOG_FILE", "/teamcity-logs/teamcity-server.log")
