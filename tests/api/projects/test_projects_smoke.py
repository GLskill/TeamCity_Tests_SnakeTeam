import allure
import pytest

from src.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestProjectsSmoke:

    @allure.id("3")  # запрос без валидного токена возвращает 401
    @allure.title("GET /projects — HTTP 401 при невалидном токене")
    def test_get_projects_unauthorized(self, admin_api_manager: ApiManager):
        admin_api_manager.project_steps.get_projects_unauthorized()

    @allure.id("4")  # есть хотя бы один проект
    @allure.title("GET /projects — HTTP 200, count >= 1")
    def test_get_projects_count(self, admin_api_manager: ApiManager):
        projects = admin_api_manager.project_steps.get_projects()
        assert projects.count >= 1

    @allure.id("6")
    @allure.title("POST /projects — создать проект, count вырос")
    @pytest.mark.usefixtures('admin_api_manager')
    def test_create_project_increases_count(self, admin_api_manager: ApiManager, get_project_request):
        count_before = admin_api_manager.project_steps.get_projects().count
        created_project = admin_api_manager.project_steps.create_project(get_project_request)
        admin_api_manager.project_steps.get_project_by_id(created_project.id)
        count_after = admin_api_manager.project_steps.get_projects().count

        assert count_after > count_before
