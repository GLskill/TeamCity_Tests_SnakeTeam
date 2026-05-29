import os
import sys
import time

from playwright.sync_api import sync_playwright
from infra.docker_compose.tc_mnt_page import MntStartedPage
from src.api.steps.preset_admin_steps import PreAdminSteps
from src.enums import UiFirstUp

sys.path.insert(0, "/app")
TC_URL = os.environ.get("UI_BASE_URL", "http://webapp:8111")
ENV_FILE = os.environ.get("ENV_FILE", "/app/.env")


def setup_teamcity_ui() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()

        (
            MntStartedPage(page)
            .open()
            .accept_first_start()
            .accept_database_setup()
            .accept_license_agreement()  # → возвращает CreateAdministratorAccount
            .create_admin_account()  # → возвращает ProjectPanel
            .check_welcome_or_favorite()
        )

        browser.close()
    print("[setup] UI wizard завершён ✓")


def wait_for_rest_api(timeout: int = 120) -> None:
    from src.api.requests.skeleton.requesters.crud_requester import CrudRequester
    from src.api.requests.skeleton.endpoint import Endpoint
    from src.api.specs.request_spec import RequestSpecs

    print("[setup] Ожидаем REST API...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            response = CrudRequester(
                request_spec=RequestSpecs.admin_basic_auth_headers(),
                endpoint=Endpoint.GET_SERVER_INFO,
                response_spec=lambda r: r,
            ).get()
            if response.status_code == 200:
                print("[setup] REST API готов ✓")
                return
        except Exception:
            pass
        time.sleep(5)
    raise RuntimeError("REST API не поднялся за отведённое время")


def create_and_save_token() -> None:
    token_value = PreAdminSteps().setup_create_token(UiFirstUp.TOKEN_NAME)

    env_dir = os.path.dirname(ENV_FILE)
    if env_dir:
        os.makedirs(env_dir, exist_ok=True)
    with open(ENV_FILE, "w") as f:
        f.write(f"TC_ADMIN_TOKEN={token_value}\n")
        f.write(f"TC_ADMIN_USERNAME={UiFirstUp.ADMIN_USERNAME}\n")
        f.write(f"TC_ADMIN_PASSWORD={UiFirstUp.ADMIN_PASSWORD}\n")
    print(f"[setup] Токен сохранён → {ENV_FILE} ✓")


if __name__ == "__main__":
    setup_teamcity_ui()
    wait_for_rest_api()
    create_and_save_token()
    print("[setup] ✅ Готово")
