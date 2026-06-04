import allure
import pytest

from src.api.classes.api_manager import ApiManager
from src.api.generators.random_data import RandomData
from src.ui.pages.project_page import ProjectPanel


@pytest.mark.ui
@pytest.mark.projects
class TestUICreateProject:

    @allure.id("70")
    @allure.title("UI — создать проект через welcome button")
    def test_create_project_via_welcome_button(self, auth_as_admin_web_no_projects, api_manager: ApiManager):
        project_name = RandomData.get_name()
        create_page = ProjectPanel(auth_as_admin_web_no_projects) \
            .click_create_project_wellcome_button() \
            .check_create_page_opened() \
            .fill_project_name(project_name)
        project_id = create_page.project_id_input.input_value()
        create_page.click_create()
        project = api_manager.project_steps.get_project_by_id_and_track(project_id)

        assert project.id == project_id
        assert project.name == project_name

    @allure.id("71")
    @allure.title("UI — создать проект через main button")
    def test_create_project_via_main_button(self, auth_as_admin_web, api_manager: ApiManager):
        project_name = RandomData.get_name()
        create_page = ProjectPanel(auth_as_admin_web) \
            .click_create_project_main_button() \
            .check_create_page_opened() \
            .fill_project_name(project_name)
        project_id = create_page.project_id_input.input_value()
        create_page.click_create()
        project = api_manager.project_steps.get_project_by_id_and_track(project_id)

        assert project.id == project_id
        assert project.name == project_name

    @allure.id("72")  #  работает если проект уже создан !
    @allure.title("UI — создать проект через dropdown button")
    def test_create_project_via_dropdown_button(self, auth_as_admin_web_with_project, api_manager: ApiManager):
        project_name = RandomData.get_name()
        create_page = ProjectPanel(auth_as_admin_web_with_project) \
            .click_create_project_dropdown_button() \
            .check_create_page_opened() \
            .fill_project_name(project_name)
        project_id = create_page.project_id_input.input_value()
        create_page.click_create()
        project = api_manager.project_steps.get_project_by_id_and_track(project_id)

        assert project.id == project_id
        assert project.name == project_name
