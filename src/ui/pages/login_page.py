import allure
from playwright.sync_api import expect

from src.enums import UiAlert
from src.api.generators.random_data import RandomData
from src.ui.pages.base_page import BasePage


class LoginPage(BasePage):

    def url(self):
        return "/login.html"

    @property
    def admin_name_input(self):
        return self.page.locator("#username")

    @property
    def admin_password_input(self):
        return self.page.locator("#password")

    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Log in")

    @property
    def error_message(self):
        return self.page.locator("#errorMessage")

    @property
    def login_to_teamcity_text(self):
        return self.page.locator("#header")

    def admin_login_with_correct_data(self, admin_username: str, admin_password: str):
        from src.ui.pages.project_page import ProjectPanel
        self.admin_name_input.fill(value=admin_username)
        self.admin_password_input.fill(value=admin_password)
        self.login_button.click()
        return ProjectPanel(self.page)

    def user_login_with_correct_data(self, username: str, password: str):
        from src.ui.pages.project_page import ProjectPanel
        self.admin_name_input.fill(value=username)
        self.admin_password_input.fill(value=password)
        self.login_button.click()
        return ProjectPanel(self.page)

    def admin_login_with_wrong_password(self, admin_username: str):
        self.admin_name_input.fill(value=admin_username)
        self.admin_password_input.fill(value=admin_username)
        self.login_button.click()
        return self

    def admin_login_multiple_times(self, times: int):
        self.admin_name_input.fill(value=RandomData.get_name())
        for x in range(times):
            self.admin_password_input.fill(value=RandomData.get_password())
            self.login_button.click()
            self.page.wait_for_load_state("domcontentloaded")
        return self

    def click_login_button(self):
        self.login_button.click()
        return self

    def check_incorrect_data_error(self):
        with allure.step("Проверить сообщение об ошибке INCORRECT_DATA"):
            expect(self.error_message).to_be_visible()
            expect(self.error_message).to_have_text(UiAlert.INCORRECT_DATA)

    def check_text_login_to_tc(self):
        with allure.step("Проверить на наличее текста 'Log in to TeamCity'"):
            expect(self.login_to_teamcity_text).to_be_visible()
            expect(self.login_to_teamcity_text).to_have_text(UiAlert.LOGIN_PAGE_VISIBLE)

    def check_limit_auth_error(self):
        with allure.step("You made 5 failed login attempts in 1m."):
            expect(self.error_message).to_be_visible()
            expect(self.error_message).to_contain_text(UiAlert.LOGIN_LIMIT_MSG)
