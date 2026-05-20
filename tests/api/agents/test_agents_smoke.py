import allure
import pytest

from src.api.classes.api_manager import ApiManager


@pytest.mark.smoke
@pytest.mark.agents
@pytest.mark.api
class TestAgentsSmoke:

    @allure.id("7")  # В окружении есть хотя бы один авторизованный агент
    @allure.title("GET /agents?locator=authorized:true — HTTP 200, >= 1 авторизованный агент")
    def test_get_authorized_agents(self, api_manager: ApiManager):
        agents = api_manager.agent_steps.get_authorized_agents()
        assert agents.count >= 1

    @allure.id("7.1")
    @allure.title("GET /agents?locator=enabled:true — список включённых агентов")
    @pytest.mark.usefixtures('enable_agent')
    def test_get_enabled_agents(self, api_manager: ApiManager, enable_agent):
        agents = api_manager.agent_steps.get_enabled_agents()
        assert agents.count >= 1

    @allure.id("7.2")
    @allure.title("GET /agents?locator=enabled:false — список выключённых агентов")
    def test_get_disabled_agents(self, api_manager: ApiManager):
        agents = api_manager.agent_steps.get_disabled_agents()
        assert agents is not None

    @allure.id("7.3")
    @allure.title("GET /agents/id:{id} — получить агента по id")
    @pytest.mark.usefixture('enable_agent')
    def test_get_agent_by_id(self, api_manager: ApiManager, enable_agent):
        agents = api_manager.agent_steps.get_enabled_agents()
        agent = api_manager.agent_steps.get_agent_by_id(agents.agent[0].id)
        assert agent.id == agents.agent[0].id
