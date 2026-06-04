import allure
import pytest

from src.api.classes.api_manager import ApiManager


@pytest.mark.smoke
@pytest.mark.server
@pytest.mark.api
class TestServerSmoke:

    @allure.id("1")
    @allure.title("GET /server — HTTP 200, поле version присутствует")
    def test_get_server_info(self, api_manager: ApiManager):
        server_info = api_manager.server_steps.get_server_info()

        assert server_info.version is not None
        assert server_info.buildDate is not None
        assert server_info.buildNumber is not None

    @allure.id("2.1")  # отсутствует токен авторизации
    @allure.title("GET /users/current — HTTP 401, отсутсвтует или не верный токен")
    def test_get_current_user_unauthorized(self, api_manager: ApiManager):
        api_manager.server_steps.get_current_user_unauthorized()

