import allure
from playwright.sync_api import expect

from src.enums import UiFirstUp
from src.ui.pages.base_page import BasePage


class CreateAdministratorAccount(BasePage):

    def url(self):
        return "/setupAdmin.html"

    @property
    def banner_create_administrator_account(self):
        return self.page.get_by_role("heading", name="Create Administrator Account")

    def check_banner_administrator(self):
        with allure.step("Проверить что страница создания администартаора открыта"):
            expect(self.banner_create_administrator_account).to_be_visible()

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
        with allure.step(f"Ввести имя Админпользовталея: '{self.admin_username}'"):
            self.admin_username_input.fill(self.admin_username)

    def fill_admin_password_and_confirm(self):
        self.admin_password = UiFirstUp.ADMIN_PASSWORD
        with allure.step("Ввести пароль и повторить  для Админа"):
            self.password_admin_input.fill(self.admin_password)
            self.confirm_password_admin_input.fill(self.admin_password)
        return self

    def create_admin_data(self, admin_username: str, admin_password: str):
        from src.ui.pages.project_page import ProjectPanel
        self.fill_admin_username.fill(value=admin_username)
        self.admin_password_input.fill(value=admin_password)
        self.create_account_button.click()
        return ProjectPanel(self.page)
