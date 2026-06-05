import allure
import pytest

from src.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestVcsRootSmoke:
    @allure.id("26")
    @allure.title("POST /vcs-roots — создание VCS Root")
    def test_create_vcs_root(self, admin_api_manager: ApiManager, vcs_root_request):
        created = admin_api_manager.vcsroot_steps.create_vcs_root(vcs_root_request)
        fetched = admin_api_manager.vcsroot_steps.get_vcs_root_by_id(created.id)

        assert fetched.id == vcs_root_request.id
        assert fetched.name == vcs_root_request.name
        assert fetched.vcsName == vcs_root_request.vcsName

    @allure.id("26.1")
    @allure.title("DELETE /vcs-roots/{locator} — удалить VCS Root, повторный GET возвращает 404")
    def test_delete_vcs_root_and_get_404(self, admin_api_manager: ApiManager, vcs_root_request):
        created = admin_api_manager.vcsroot_steps.create_vcs_root(vcs_root_request)
        admin_api_manager.vcsroot_steps.delete_vcs_root(created.id)
        admin_api_manager.vcsroot_steps.get_deleted_vcs_root(created.id)
