import os
import sys

sys.path.insert(0, "/app")

from infra.docker_compose.setup.config import ENV_FILE
from infra.docker_compose.setup.ui_wizard import setup_teamcity_ui
from infra.docker_compose.setup.rest_api import wait_for_rest_api
from infra.docker_compose.setup.agent import authorize_agent
from infra.docker_compose.setup.env_writer import save_token_to_env

if __name__ == "__main__":
    if os.path.exists(ENV_FILE):
        os.remove(ENV_FILE)
        print(f"[setup] Старый {ENV_FILE} удалён")

    token = setup_teamcity_ui()
    wait_for_rest_api(token)
    authorize_agent(token)
    save_token_to_env(token)
    print("[setup] ✅ Готово")
