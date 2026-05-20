import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()


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
