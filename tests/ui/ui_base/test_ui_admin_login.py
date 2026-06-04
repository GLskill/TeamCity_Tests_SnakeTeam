import allure
import pytest
from playwright.sync_api import Page

from src.ui.pages.login_page import LoginPage


@pytest.mark.ui
class TestLoginAdmin:

    @allure.id("51")
    @allure.title("UI — логин админа с корректными данными")
    def test_admin_login_with_correct_data(self, page: Page, ui_system_admin):
        LoginPage(page).open() \
            .admin_login_with_correct_data(ui_system_admin["username"], ui_system_admin["password"]) \
            .check_welcome_or_favorite()

    @allure.id("52")
    @allure.title("UI — логин с неверным паролем")
    def test_admin_login_with_wrong_password(self, page: Page, ui_system_admin):
        LoginPage(page).open() \
            .admin_login_with_wrong_password(ui_system_admin["username"]) \
            .check_incorrect_data_error()

    @allure.id("53")
    @allure.title("UI — логин с пустым логином и паролем")
    def test_login_with_empty_credentials(self, page: Page, ui_system_admin):
        LoginPage(page).open() \
            .click_login_button() \
            .check_incorrect_data_error()

    @allure.id("55")
    @allure.title("UI — логаут админа")
    def test_admin_logout(self, page: Page, ui_system_admin):
        LoginPage(page).open() \
            .admin_login_with_correct_data(ui_system_admin["username"], ui_system_admin["password"]) \
            .click_go_to_log_out() \
            .check_text_login_to_tc()

    @allure.id("56")
    @allure.title("UI — 5 раз неверный логин, получаем ошибку лимита авторизации")
    def test_five_time_loging_get_error(self, page: Page, ui_system_admin):
        LoginPage(page).open() \
            .admin_login_multiple_times(times=6) \
            .check_limit_auth_error()