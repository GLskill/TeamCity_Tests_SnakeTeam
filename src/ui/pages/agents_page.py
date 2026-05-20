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
        with allure.step("Проверить наличие текста 'Overview' на странице агентов"):
            expect(self.agents_page_text).to_be_visible()
            expect(self.agents_page_text).to_have_text(UiAlert.AGENTS_OVERVIEW)
        return self

