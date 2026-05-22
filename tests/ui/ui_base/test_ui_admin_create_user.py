import allure
import pytest

from src.api.classes.api_manager import ApiManager
from src.ui.pages.administration_page import AdminPanel


@pytest.mark.ui
@pytest.mark.users
class TestUiAdminCreateUser:
    @allure.id("79")
    @allure.title("UI — открыть страницу создания пользователя")
    def test_auth_as_admin_and_open_user_page(self, auth_as_admin_web):
        AdminPanel(auth_as_admin_web) \
            .open() \
            .click_switch_to_users() \
            .check_users_page_opened() \
            .click_create_user() \
            .check_create_user_page_opened()

    @allure.id("80")
    @allure.title("UI — создать пользователя через форму")
    def test_create_user_via_admin(self, auth_as_admin_and_open_user_page, api_manager: ApiManager):
        auth_as_admin_and_open_user_page \
            .fill_username() \
            .fill_password_and_retype() \
            .click_create() \
            .check_users_page_opened()

        user = api_manager.user_steps.admin_get_user_by_username(auth_as_admin_and_open_user_page.username)
        api_manager.user_steps.created_objects.append(user)
        assert user.username == auth_as_admin_and_open_user_page.username

    @allure.id("81")
    @allure.title("UI — отмена создания пользователя")
    def test_cancel_create_user_via_admin(self, auth_as_admin_and_open_user_page, api_manager: ApiManager):
        auth_as_admin_and_open_user_page \
            .fill_username() \
            .fill_password_and_retype() \
            .click_cancel() \
            .check_users_page_opened()

        api_manager.user_steps.admin_get_deleted_user_by_username(auth_as_admin_and_open_user_page.username)
