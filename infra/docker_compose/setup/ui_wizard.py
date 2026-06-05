from playwright.sync_api import sync_playwright

from src.ui.pages.tc_mnt_page import MntStartedPage
from infra.docker_compose.setup.token import get_super_user_token


def setup_teamcity_ui() -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()

        (
            MntStartedPage(page)
            .open()
            .accept_first_start()
            .accept_database_setup()
            .accept_license_agreement()
            .check_banner_administrator()
        )

        token = get_super_user_token()
        browser.close()

    print("[setup] UI wizard завершён ✓")
    return token
