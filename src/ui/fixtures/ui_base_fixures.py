import os
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page

from src.api.classes.api_manager import ApiManager
from src.api.configs.config import Config
from src.api.generators.random_data import RandomData
from src.ui.pages.administration_page import AdminPanel

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


@pytest.fixture
def user_credentials():
    return {
        "username": RandomData.get_name().lower(),
        "password": RandomData.get_password()
    }


@pytest.fixture
def created_user_via_api(api_manager: ApiManager, user_request):
    return api_manager.user_steps.admin_create_user(user_request)


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

    yield page

    page.close()


@pytest.fixture()
def auth_as_admin_web_with_project(context: BrowserContext, admin_username, admin_password, api_manager,
                                   target_project) -> Page:
    context.add_cookies(_get_session_cookie(admin_username, admin_password))
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).rstrip("/")
    page.goto(f"{base_url}/favorite/projects", wait_until="domcontentloaded")

    yield page

    page.close()


@pytest.fixture
def auth_as_admin_and_open_user_page(auth_as_admin_web, user_request, api_manager):
    user = api_manager.user_steps.admin_create_user(user_request)
    users_page = (
        AdminPanel(auth_as_admin_web)
        .open()
        .click_switch_to_users()
        .check_users_page_opened()
    )
    users_page.user = user
    return users_page


@pytest.fixture
def auth_as_admin_and_open_create_user_page(auth_as_admin_web):
    return (
        AdminPanel(auth_as_admin_web)
        .open()
        .click_switch_to_users()
        .check_users_page_opened()
        .click_create_user()
        .check_create_user_page_opened()
    )
