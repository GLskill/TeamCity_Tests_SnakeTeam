from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv(dotenv_path=Path(__file__).parents[3] / ".env", override=True)


@pytest.fixture()
def page(page: Page) -> Page:
    page.set_viewport_size({"width": 1920, "height": 1080})
    return page
