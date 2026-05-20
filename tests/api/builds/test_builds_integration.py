import allure
import pytest

from src.api.classes.api_manager import ApiManager
from src.enums import BuildParams
from src.api.models.requests import BuildCancelRequest, QueueBuildRequest
from src.api.models.responses import QueueBuildResponse


@pytest.mark.integraion
@pytest.mark.builds
@pytest.mark.api
class TestBuildIntegration:
    @allure.id("8")
    @allure.title("Отмена билда в очереди (queued)")
    @pytest.mark.usefixtures('queue_build', 'api_manager', 'queued_build_cancel_request')
    def test_cancel_queued_build(
            self,
            api_manager: ApiManager,
            queue_build: QueueBuildResponse,
            queued_build_cancel_request: BuildCancelRequest
    ):
        canceled_build = api_manager.build_steps.cancel_queued_build(queued_build_cancel_request, queue_build.id)
        get_build = api_manager.build_steps.get_queued_build_by_id(queue_build.id)

        assert canceled_build.state == get_build.state
        assert canceled_build.status == get_build.status

    @allure.id("9")
    @allure.title("Отмена запущенного билда (running)")
    @pytest.mark.usefixtures('enable_agent', 'api_manager', 'queue_build', 'running_build_cancel_request')
    def test_cancel_running_build(
            self,
            api_manager: ApiManager,
            queue_build: QueueBuildResponse,
            running_build_cancel_request: BuildCancelRequest
    ):
        canceled_build = api_manager.build_steps.cancel_running_build(running_build_cancel_request, queue_build.id)
        get_build = api_manager.build_steps.get_queued_build_by_id(queue_build.id)

        assert canceled_build.state == get_build.state
        assert canceled_build.status == get_build.status

    @allure.id("22")
    @allure.title("POST /buildTypes — создать build configuration")
    def test_create_build_configuration(self, api_manager: ApiManager, build_type_request):
        created = api_manager.build_steps.create_build_type(build_type_request)
        fetched = api_manager.build_steps.get_build_type_by_id(created.id)

        assert fetched.id == build_type_request.id
        assert fetched.name == build_type_request.name

    @allure.id("22.1")
    @allure.title("DELETE /buildTypes/{locator} — удалить build type, повторный GET возвращает 404")
    def test_delete_build_type_and_get_404(self, api_manager: ApiManager, build_type):
        api_manager.build_steps.delete_build_type(build_type.id)
        api_manager.build_steps.get_deleted_build_type(build_type.id)

    @allure.id("10")
    @allure.title("Запуск custom build (параметры, ветка, агент)")
    @pytest.mark.usefixtures('enable_agent', 'api_manager', 'custom_build_request')
    def test_start_custom_build(
            self,
            api_manager: ApiManager,
            custom_build_request: QueueBuildRequest,
            enable_agent
    ):
        response = api_manager.build_steps.add_build_to_queue(custom_build_request)
        get_build = api_manager.build_steps.get_queued_build_by_id(response.id)

        assert custom_build_request.comment.text == get_build.comment.text

    @allure.id("23")
    @allure.title("POST /projects/{projectLocator}/buildTypes — копирование build configuration")
    def test_copy_build_configuration(self, api_manager: ApiManager, build_type, copy_build_request, created_project):
        copied = api_manager.build_steps.copy_build_type_to_project(created_project.id, copy_build_request)
        fetched_copy = api_manager.build_steps.get_build_type_by_id(copied.id)

        assert fetched_copy.id == copy_build_request.id
        assert fetched_copy.project is not None
        assert fetched_copy.project.get("id") == created_project.id

    @allure.id("24")
    @allure.title("PUT /buildTypes/{buildTypeLocator}/paused — приостановка build configuration")
    def test_pause_build_configuration(self, api_manager: ApiManager, build_type):
        assert api_manager.build_steps.get_build_type_paused(build_type.id) is False

        api_manager.build_steps.set_build_type_paused(build_type.id, True)
        assert api_manager.build_steps.get_build_type_paused(build_type.id) is True

    @allure.id("25")
    @allure.title("PUT /buildTypes/{buildTypeLocator}/parameters/{name} — изменение параметра build configuration")
    def test_update_build_configuration_parameter(self, api_manager: ApiManager, build_type):
        api_manager.build_steps.set_build_type_parameter(build_type.id, BuildParams.PARAM_NAME, BuildParams.PARAM_VALUE)
        parameter = api_manager.build_steps.get_build_type_parameter(build_type.id, BuildParams.PARAM_NAME)
        assert parameter.get("value") == BuildParams.PARAM_VALUE

    @allure.id("28")
    @allure.title("POST /buildTypes/{locator}/move — перемещение build configuration в другой проект")
    def test_move_build_configuration(self, api_manager: ApiManager, build_type, target_project):
        api_manager.build_steps.move_build_type_to_project(build_type.id, target_project.id)
        fetched = api_manager.build_steps.get_build_type_by_id(build_type.id)

        assert fetched.project.get("id") == target_project.id

    @allure.id("29")
    @allure.title("GET /buildTypes?locator=affectedProject — рекурсивный поиск build configs")
    def test_get_build_by_affected_project(self, api_manager: ApiManager, build_type, sub_build_type, created_project):
        build_types = api_manager.build_steps.get_build_by_affected_project(created_project.id)

        assert build_type.id in build_types.get_ids()
        assert sub_build_type.id in build_types.get_ids()