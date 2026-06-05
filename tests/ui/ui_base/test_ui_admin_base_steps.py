import allure
import pytest
from src.ui.pages.project_page import ProjectPanel


@pytest.mark.ui
class TestLoginAdmin:
    @allure.id("57")
    @allure.title("UI — админ жмёт кнопку создать проект через wellcome button")
    def test_admin_click_welcome_create_project_button(self, auth_as_system_admin):
        ProjectPanel(auth_as_system_admin) \
            .click_create_project_wellcome_button() \
            .check_create_page_opened()

    @allure.id("58")
    @allure.title("UI — админ жмёт кнопку создать проект через main button")
    def test_admin_click_main_create_project_button(self, auth_as_system_admin):
        ProjectPanel(auth_as_system_admin) \
            .click_create_project_main_button() \
            .check_create_page_opened()

    @allure.id("59")  # появится вместо приветсвенной кнопки создать проект
    @allure.title("UI — админ жмёт кнопку создать проект через dropdown button")
    def test_admin_click_dropdown_create_project_button(self, auth_as_system_admin_with_project):
        ProjectPanel(auth_as_system_admin_with_project) \
            .click_create_project_dropdown_button() \
            .check_create_page_opened()

    @allure.id("60")
    @allure.title("UI — админ жмёт кнопку Changes")
    def test_admin_click_changes_button(self, auth_as_system_admin):
        ProjectPanel(auth_as_system_admin) \
            .click_switch_to_changes() \
            .check_changes_page()

    @allure.id("61")
    @allure.title("UI — админ жмёт кнопку Agents")
    def test_admin_click_agents_button(self, auth_as_system_admin):
        ProjectPanel(auth_as_system_admin) \
            .click_switch_to_agents() \
            .check_agents_page()

    @allure.id("62")
    @allure.title("UI — админ жмёт кнопку Queue")
    def test_admin_click_queue_button(self, auth_as_system_admin):
        ProjectPanel(auth_as_system_admin) \
            .click_switch_to_queue() \
            .check_queue_page()

    @allure.id("63")
    @allure.title("UI — админ жмёт кнопку Administration")
    def test_admin_click_administration_button(self, auth_as_system_admin):
        ProjectPanel(auth_as_system_admin) \
            .click_switch_to_administration() \
            .check_administration_page()


