import allure
import pytest

from src.api.classes.api_manager import ApiManager


@pytest.mark.smoke
@pytest.mark.vcs_root
@pytest.mark.api
class TestVcsRootSmoke:
    @allure.id("26")
    @allure.title("POST /vcs-roots — создание VCS Root")
    def test_create_vcs_root(self, api_manager: ApiManager, vcs_root_request):
        created = api_manager.vcsroot_steps.create_vcs_root(vcs_root_request)
        fetched = api_manager.vcsroot_steps.get_vcs_root_by_id(created.id)

        assert fetched.id == vcs_root_request.id
        assert fetched.name == vcs_root_request.name
        assert fetched.vcsName == vcs_root_request.vcsName

    @allure.id("26.1")
    @allure.title("DELETE /vcs-roots/{locator} — удалить VCS Root, повторный GET возвращает 404")
    def test_delete_vcs_root_and_get_404(self, api_manager: ApiManager, vcs_root_request):
        created = api_manager.vcsroot_steps.create_vcs_root(vcs_root_request)
        api_manager.vcsroot_steps.delete_vcs_root(created.id)
        api_manager.vcsroot_steps.get_deleted_vcs_root(created.id)
