import allure
import pytest

from src.api.classes.api_manager import ApiManager


@pytest.mark.projects
@pytest.mark.integration
@pytest.mark.api
class TestProjectIntegration:
    @allure.id("20")  # запрос с жёсткими данными
    @allure.title("POST /projects — создать проект с заданными атрибутами")
    def test_create_project_with_expected_attributes(self, api_manager: ApiManager, get_project_request):
        created = api_manager.project_steps.create_project(get_project_request)
        fetched = api_manager.project_steps.get_project_by_id(created.id)

        assert fetched.id == get_project_request.id
        assert fetched.name == get_project_request.name

    @allure.id("21")
    @allure.title("DELETE /projects/{locator} — удалить проект, повторный GET возвращает 404")
    def test_delete_project_and_get_404(self, api_manager: ApiManager, created_project, project_not_found):
        api_manager.project_steps.delete_project(created_project.id)
        api_manager.project_steps.get_deleted_project(created_project.id)

    @allure.id("29.1")
    @allure.title("POST /projects — создание подпроекта с parentProject")
    def test_create_sub_project(self, api_manager: ApiManager, created_project, sub_project_request):
        created = api_manager.project_steps.create_project(sub_project_request)
        fetched = api_manager.project_steps.get_project_by_id(created.id)

        assert fetched.id == sub_project_request.id
        assert fetched.parentProjectId == created_project.id

    @allure.id("27")
    @allure.title("PUT /projects/{projectLocator}/archived — архивация проекта")
    def test_archive_project(self, api_manager: ApiManager, created_project, archive_project):
        archive_project(created_project.id, True)
        fetched_archived = api_manager.project_steps.get_project_by_id(created_project.id)
        assert fetched_archived.archived is True
