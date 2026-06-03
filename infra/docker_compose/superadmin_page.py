import allure
from playwright.sync_api import expect
from src.ui.pages.base_page import BasePage

WAIT_TIMEOUT = 120_000


class LoginAsSuperAdmin(BasePage):

    def url(self):
        return "/login.html?super=1"

    @property
    def banner_log_in_as_super_admin(self):
        return self.page.get_by_role("heading", name="Log in as Super user")

    def check_banner_administrator(self):
        with allure.step("Проверить что страница входа как суперадмин открыта"):
            expect(self.banner_log_in_as_super_admin).to_be_visible(timeout=WAIT_TIMEOUT)

    @property
    def super_admin_password_input(self):
        return self.page.locator("#password")

    def input_super_admin_token(self, token: str):
        with allure.step("Ввести токен суперадмина из логов контейнера"):
            self.super_admin_password_input.fill(token)
        return self

    @property
    def log_in_super_admin_button(self):
        return self.page.get_by_role("button", name="Log in")

    def click_log_in_as_super_admin_button(self):
        with allure.step("Нажать кнопку Log In для суперадмина"):
            self.log_in_super_admin_button.click()
            self.page.wait_for_load_state("networkidle")
        return self

    def login_as_super_admin(self, token: str):
        from src.ui.pages.project_page import ProjectPanel
        self.check_banner_administrator()
        self.input_super_admin_token(token)
        self.click_log_in_as_super_admin_button()
        return ProjectPanel(self.page)