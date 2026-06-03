import allure
from playwright.sync_api import expect

from src.enums import UiFirstUp
from src.ui.pages.base_page import BasePage

WAIT_TIMEOUT = 120_000


class CreateAdministratorAccount(BasePage):

    def url(self):
        return "/setupAdmin.html"

    @property
    def banner_create_administrator_account(self):
        return self.page.get_by_role("heading", name="Create Administrator Account")

    def check_banner_administrator(self):
        with allure.step("Проверить что страница создания администратора открыта"):
            expect(self.banner_create_administrator_account).to_be_visible(timeout=WAIT_TIMEOUT)

    @property
    def admin_username_input(self):
        return self.page.locator("#input_teamcityUsername")

    @property
    def password_admin_input(self):
        return self.page.locator("#password1")

    @property
    def confirm_password_admin_input(self):
        return self.page.locator("#retypedPassword")

    @property
    def create_account_button(self):
        return self.page.get_by_role("button", name="Create Account")

    def fill_admin_username(self):
        self.admin_username = UiFirstUp.ADMIN_USERNAME
        with allure.step(f"Ввести имя администратора: '{self.admin_username}'"):
            self.admin_username_input.fill(self.admin_username)
        return self

    def fill_admin_password_and_confirm(self):
        self.admin_password = UiFirstUp.ADMIN_PASSWORD
        with allure.step("Ввести пароль и подтверждение для администратора"):
            self.password_admin_input.fill(self.admin_password)
            self.confirm_password_admin_input.fill(self.admin_password)
        return self

    def click_create_account_button(self):
        with allure.step("Нажать кнопку Create Account"):
            self.create_account_button.click()
            self.page.wait_for_load_state("networkidle")
        return self

    def create_admin_account(self):
        from src.ui.pages.project_page import ProjectPanel
        self.check_banner_administrator()
        self.fill_admin_username()
        self.fill_admin_password_and_confirm()
        self.click_create_account_button()
        return ProjectPanel(self.page)

    @property
    def link_create_administrator_account(self):
        return self.page.get_by_role("link", name="Login as Super user")

    def click_link_login_via_super_admin(self):
        from infra.docker_compose.superadmin_page import LoginAsSuperAdmin
        self.link_create_administrator_account.click()
        self.page.wait_for_load_state("networkidle")
        return LoginAsSuperAdmin(self.page)

