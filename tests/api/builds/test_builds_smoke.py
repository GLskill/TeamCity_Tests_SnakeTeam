import allure
import pytest

from src.api.classes.api_manager import ApiManager
from src.enums import BuildState


@pytest.mark.smoke
@pytest.mark.builds
@pytest.mark.api
class TestBuildsSmoke:
    @allure.id("5.1")
    @allure.title("POST /buildTypes — создать build configs, id и name совпадают")
    def test_create_build_type(self, api_manager: ApiManager, build_type_request):
        created_build_type = api_manager.build_steps.create_build_type(build_type_request)
        fetched_build_type = api_manager.build_steps.get_build_type_by_id(created_build_type.id)

        assert fetched_build_type.id == build_type_request.id
        assert fetched_build_type.name == build_type_request.name

    @allure.id("5")
    @allure.title("POST /buildQueue — поставить сборку в очередь, state=queued")
    def test_queue_build_state_queued(self, api_manager: ApiManager, queue_build_request):
        queued_build = api_manager.build_steps.add_build_to_queue(queue_build_request)
        fetched_queued_build = api_manager.build_steps.get_queued_build_by_id(queued_build.id)

        assert fetched_queued_build.state == BuildState.QUEUED
