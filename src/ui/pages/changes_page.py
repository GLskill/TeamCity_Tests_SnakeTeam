import allure
from playwright.sync_api import expect

from src.enums import UiAlert
from src.ui.pages.base_page import BasePage


class ChangesPanel(BasePage):
    def url(self):
        return "/changes"

    @property
    def changes_page(self):
        return self.page.locator("h1.ChangesPage-module__heading--Pa")

    def check_changes_page(self):
        with allure.step("Проверить наличее текста 'Changes' "):
            expect(self.changes_page).to_be_visible()
            expect(self.changes_page).to_have_text(UiAlert.CHANGES)
