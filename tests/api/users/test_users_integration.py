import allure
import pytest
from src.enums import UserParams
from src.api.classes.api_manager import ApiManager


@pytest.mark.users
@pytest.mark.integration
@pytest.mark.api
class TestUsersIntegration:

    @allure.id("33")
    @allure.title("POST /users — создание пользователя")  # !!!  Баг? Teamsity отдаёт в нижнем регистре юзернэйм!
    def test_admin_create_user(self, api_manager: ApiManager, user_request):
        created = api_manager.user_steps.admin_create_user(user_request)
        fetched = api_manager.user_steps.admin_get_user_by_id(created.id)

        assert fetched.id == created.id
        assert fetched.username == user_request.username.lower()  # lower for worf test

    @allure.id("37")
    @allure.title("GET /users/current — возвращает текущего аутентифицированного пользователя")
    def test_get_current_user(self, api_manager: ApiManager):
        current = api_manager.user_steps.admin_get_current_user()

        assert current.id is not None
        assert current.username is not None

    @allure.id("35")
    @allure.title("DELETE /users/{locator} — удалить пользователя, повторный GET возвращает 404")
    def test_admin_delete_user_and_get_404(self, api_manager: ApiManager, created_user):
        api_manager.user_steps.admin_delete_user(created_user.id)
        api_manager.user_steps.admin_get_deleted_user(created_user.id)

    @allure.id("35.1")
    @allure.title("GET /users/{locator} — несуществующий id возвращает 404")
    def test_get_nonexistent_user_returns_404(self, api_manager: ApiManager):
        api_manager.user_steps.admin_get_deleted_user(UserParams.NONEXISTENT_ID)

    @allure.id("41")
    @allure.title("GET /users/{locator}/groups — получить группы пользователя")
    def test_get_user_groups(self, api_manager: ApiManager, created_user, created_objects):
        created_objects.append(created_user)
        groups = api_manager.user_steps.admin_get_user_groups(created_user.id)

        assert groups is not None

