import allure
from playwright.sync_api import expect

from src.api.generators.random_data import RandomData
from src.ui.pages.base_page import BasePage


class AdminCreateUserPage(BasePage):
    def url(self):
        return "/admin/createUser.html"

    @property
    def page_title(self):
        return self.page.locator("#restPageTitle span.contentWrapper", has_text="Create a New User Account")

    @property
    def username_input(self):
        return self.page.locator("#input_teamcityUsername")

    @property
    def full_name_input(self):
        return self.page.locator("#name")

    @property
    def email_input(self):
        return self.page.locator("#input_teamcityEmail")

    @property
    def password_input(self):
        return self.page.locator("#password1")

    @property
    def retype_password_input(self):
        return self.page.locator("#retypedPassword")

    @property
    def submit_button(self):
        return self.page.locator("input[name='submitCreateUser']")

    @property
    def cancel_button(self):
        return self.page.locator("a.btn.cancel[href*='item=users']")

    def check_create_user_page_opened(self):
        with allure.step("Проверить что открыта страница создания пользователя"):
            expect(self.page_title).to_be_visible()
        return self

    def fill_username(self):
        self.username = RandomData.get_name().lower()
        with allure.step(f"Ввести имя пользователя: '{self.username}'"):
            self.username_input.fill(self.username)
        return self

    def fill_password_and_retype(self):
        self.password = RandomData.get_password()
        with allure.step("Ввести пароль и повторить"):
            self.password_input.fill(self.password)
            self.retype_password_input.fill(self.password)
        return self

    def click_create(self):
        with allure.step("Нажать кнопку Create User"):
            self.submit_button.click()
        from src.ui.pages.admin_users_page import UsersPage
        return UsersPage(self.page)

    def click_cancel(self):
        with allure.step("Нажать кнопку Cancel"):
            self.cancel_button.click()
        from src.ui.pages.admin_users_page import UsersPage
        return UsersPage(self.page)
