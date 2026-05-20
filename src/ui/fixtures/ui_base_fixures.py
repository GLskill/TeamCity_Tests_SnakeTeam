import os
import pytest
import requests
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page
from src.api.configs.config import Config

load_dotenv(dotenv_path=Path(__file__).parents[3] / ".env", override=True)


@pytest.fixture()
def page(page: Page) -> Page:
    page.set_viewport_size({"width": 1920, "height": 1080})
    return page


@pytest.fixture()
def admin_username() -> str:
    return os.getenv("TC_ADMIN_USERNAME")


@pytest.fixture()
def admin_password() -> str:
    return os.getenv("TC_ADMIN_PASSWORD")


def _get_session_cookie(username: str, password: str) -> list[dict]:
    assert username and password, (
        f"Credentials не загружены: username={username!r}, password={password!r}"
    )

    base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).rstrip("/")
    session = requests.Session()
    response = session.get(
        url=f"{base_url}/httpAuth/app/rest/server",
        auth=(username, password),
    )
    assert response.status_code == 200, (
        f"Basic Auth не удался: {response.status_code}\n{response.text[:200]}"
    )
    cookies = [
        {"name": c.name, "value": c.value, "url": base_url}
        for c in session.cookies
    ]
    assert cookies, "Basic Auth прошёл, но куки пустые"
    return cookies


@pytest.fixture()
def auth_as_admin_web(context: BrowserContext, admin_username, admin_password) -> Page:
    context.add_cookies(_get_session_cookie(admin_username, admin_password))

    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})

    base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).rstrip("/")
    page.goto(f"{base_url}/favorite/projects", wait_until="domcontentloaded")

    return page