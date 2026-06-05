import allure
from playwright.sync_api import expect

from src.enums import UiAlert
from src.ui.pages.base_page import BasePage


class AgentsPanel(BasePage):
    def url(self):
        return "/agents/overview"

    @property
    def agents_page_text(self):
        return self.page.locator("h1.PageTitle-module__title--gU")

    def check_agents_page(self):
        with allure.step("Проверить что открылась страница агентов"):
            expect(self.agents_page_text).to_be_visible()
            actual_text = self.agents_page_text.inner_text()
            expected = {UiAlert.AGENTS_OVERVIEW, UiAlert.AGENTS_FAVORITE_POOLS}
            assert actual_text in expected, (
                f"Ожидался один из текстов {expected}, получен: '{actual_text}'"
            )
        return self

