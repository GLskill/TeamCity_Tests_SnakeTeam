import allure
import pytest
from playwright.sync_api import BrowserContext, Page

from src.api.classes.api_manager import ApiManager
from src.api.configs.config import Config
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import CreateUserRequest
from src.ui.pages.administration_page import AdminPanel

import requests


def _get_session_cookie_for_user(username: str, password: str) -> list[dict]:
    base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).rstrip("/")
    session = requests.Session()
    response = session.get(
        url=f"{base_url}/httpAuth/app/rest/server",
        auth=(username, password),
    )
    assert response.status_code == 200, (
        f"Basic Auth не удался для '{username}': {response.status_code}\n{response.text[:200]}"
    )
    cookies = [
        {"name": c.name, "value": c.value, "url": base_url}
        for c in session.cookies
    ]
    assert cookies, f"Basic Auth прошёл для '{username}', но куки пустые"
    return cookies


@pytest.fixture()
def ui_system_admin(created_objects):
    api_manager = ApiManager(created_objects)
    user_request: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
    user = api_manager.super_user_steps.create_system_admin(user_request)

    allure.attach(
        f"username: {user.username}\npassword: {user_request.password}\nid: {user.id}",
        name="System Admin credentials",
        attachment_type=allure.attachment_type.TEXT,
    )

    yield {
        "username": user.username,
        "password": user_request.password,
        "id": user.id,
    }
    api_manager.super_user_steps.delete_system_admin(user.id)


@pytest.fixture()
def auth_as_system_admin(context: BrowserContext, ui_system_admin) -> Page:
    base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).rstrip("/")
    cookies = _get_session_cookie_for_user(
        username=ui_system_admin["username"],
        password=ui_system_admin["password"],
    )
    context.add_cookies(cookies)
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto(f"{base_url}/favorite/projects", wait_until="domcontentloaded")

    yield page
    page.close()


@pytest.fixture()
def auth_as_system_admin_and_open_create_user_page(auth_as_system_admin):
    return (
        AdminPanel(auth_as_system_admin)
        .open()
        .click_switch_to_users()
        .check_users_page_opened()
        .click_create_user()
        .check_create_user_page_opened()
    )


@pytest.fixture()
def auth_as_system_admin_and_open_user_page(auth_as_system_admin, user_request, api_manager):
    user = api_manager.user_steps.admin_create_user(user_request)
    users_page = (
        AdminPanel(auth_as_system_admin)
        .open()
        .click_switch_to_users()
        .check_users_page_opened()
    )
    users_page.user = user
    return users_page


@pytest.fixture()
def auth_as_system_admin_no_projects(context: BrowserContext, ui_system_admin) -> Page:
    manager = ApiManager([])
    projects = manager.project_steps.get_all_projects()
    for project in (projects.project or []):
        project_id = project["id"] if isinstance(project, dict) else project.id
        if project_id != "_Root":
            try:
                manager.project_steps.delete_project(project_id)
            except Exception:
                pass

    base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).rstrip("/")
    cookies = _get_session_cookie_for_user(
        username=ui_system_admin["username"],
        password=ui_system_admin["password"],
    )
    context.add_cookies(cookies)

    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto(f"{base_url}/favorite/projects", wait_until="domcontentloaded")

    yield page

    page.close()


@pytest.fixture()
def auth_as_system_admin_with_project(context: BrowserContext, ui_system_admin, api_manager, target_project) -> Page:
    base_url = str(Config.get("UI_BASE_URL", "http://localhost:8111")).rstrip("/")
    cookies = _get_session_cookie_for_user(
        username=ui_system_admin["username"],
        password=ui_system_admin["password"],
    )
    context.add_cookies(cookies)

    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto(f"{base_url}/favorite/projects", wait_until="domcontentloaded")

    yield page
    page.close()
