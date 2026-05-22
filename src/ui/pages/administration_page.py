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

    @property
    def users_tab(self):
        return self.page.locator('[data-tab-id="users"] a')

    def check_administration_page(self):
        with allure.step("Проверить наличие текста 'Administration' на странице администрирования"):
            expect(self.admin_page_text).to_be_visible()
            expect(self.admin_page_text).to_have_text(UiAlert.ADMINISTRATION)
        return self

    def click_switch_to_users(self):
        with allure.step("Перейти на вкладку Users"):
            self.users_tab.click()
        from src.ui.pages.admin_users_page import UsersPage
        return UsersPage(self.page)
