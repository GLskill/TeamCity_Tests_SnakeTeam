import allure
from playwright.sync_api import expect

from src.enums import UiAlert
from src.ui.pages.base_page import BasePage


class AdminPanel(BasePage):
    def url(self):
        return "/admin/admin.html"

    @property
    def admin_page_text(self):
        return self.page.locator("b.admin-menu-title")

    def check_administration_page(self):
        with allure.step("Проверить наличие текста 'Administration' на странице администрирования"):
            expect(self.admin_page_text).to_be_visible()
            expect(self.admin_page_text).to_have_text(UiAlert.ADMINISTRATION)
        return self
