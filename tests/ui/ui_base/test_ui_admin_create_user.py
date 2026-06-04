import allure
import pytest

from src.api.classes.api_manager import ApiManager
from src.ui.pages.administration_page import AdminPanel
from src.ui.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.users
class TestUiAdminCreateUser:

    @allure.id("79")
    @allure.title("UI — открыть страницу создания пользователя")
    def test_auth_as_admin_and_open_user_page(self, auth_as_system_admin):
        AdminPanel(auth_as_system_admin) \
            .open() \
            .click_switch_to_users() \
            .check_users_page_opened() \
            .click_create_user() \
            .check_create_user_page_opened()

    @allure.id("80")
    @allure.title("UI — пользователь созданный через API отображается в списке")
    def test_create_user_via_admin(self, auth_as_system_admin_and_open_user_page):
        users_page = auth_as_system_admin_and_open_user_page
        users_page.check_user_exists_in_list(users_page.user.username)

    @allure.id("81")
    @allure.title("UI — отмена создания пользователя")
    def test_cancel_create_user_via_admin(self, auth_as_system_admin_and_open_create_user_page, api_manager: ApiManager):
        auth_as_system_admin_and_open_create_user_page \
            .fill_username() \
            .fill_password_and_retype() \
            .click_cancel() \
            .check_users_page_opened()
        api_manager.user_steps.admin_get_deleted_user_by_username(auth_as_system_admin_and_open_create_user_page.username)

    @allure.id("82")
    @allure.title("E2E — пользователь созданный через API может залогиниться через UI")
    def test_user_created_via_api_can_login_via_ui(self, page, user_request, api_manager: ApiManager, ui_system_admin):
        password = user_request.password
        user = api_manager.user_steps.admin_create_user(user_request)
        LoginPage(page) \
            .open() \
            .user_login_with_correct_data(user.username, password) \
            .check_welcome_or_favorite()
