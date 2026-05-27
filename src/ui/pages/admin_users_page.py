import allure
from playwright.sync_api import expect
from src.ui.pages.base_page import BasePage


class UsersPage(BasePage):
    def url(self):
        return "/admin/admin.html?item=users"

    @property
    def users_page_title(self):
        return self.page.locator("span.contentWrapper", has_text="Users")

    @property
    def create_user_button(self):
        return self.page.locator("a.btn", has_text="Create user account")

    def check_users_page_opened(self):
        with allure.step("Проверить что открыта страница Users"):
            expect(self.users_page_title).to_be_visible()
        return self

    def click_create_user(self):
        with allure.step("Нажать кнопку Create user account"):
            self.create_user_button.click()
        from src.ui.pages.admin_create_user_page import AdminCreateUserPage
        return AdminCreateUserPage(self.page)

    def check_user_exists_in_list(self, username: str):
        with allure.step(f"Проверить что пользователь '{username}' отображается в списке"):
            user_row = self.page.locator(f"td a[href*='editUser']:has-text('{username}')")
            expect(user_row).to_be_visible()
        return self

