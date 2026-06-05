import allure
import pytest

from src.api.classes.api_manager import ApiManager
from src.api.models.responses import AgentResponse


@pytest.mark.api
class TestAgentsSmoke:

    @allure.id("7")
    @allure.title("GET /agents?locator=authorized:true — HTTP 200, >= 1 авторизованный агент")
    def test_get_authorized_agents(self, admin_api_manager: ApiManager, authorized_agent: AgentResponse):
        agents = admin_api_manager.agent_steps.get_authorized_agents()
        assert agents.count >= 1

    @allure.id("7.1")
    @allure.title("GET /agents?locator=enabled:true — список включённых агентов")
    def test_get_enabled_agents(self, admin_api_manager: ApiManager, authorized_agent: AgentResponse):
        agents = admin_api_manager.agent_steps.get_enabled_agents()
        assert agents.count >= 1

    @allure.id("7.2")
    @allure.title("GET /agents?locator=enabled:false — список выключённых агентов")
    def test_get_disabled_agents(self, admin_api_manager: ApiManager):
        agents = admin_api_manager.agent_steps.get_disabled_agents()
        assert agents is not None

    @allure.id("7.3")
    @allure.title("GET /agents/id:{id} — получить агента по id")
    def test_get_agent_by_id(self, admin_api_manager: ApiManager, authorized_agent: AgentResponse):
        agent = admin_api_manager.agent_steps.get_agent_by_id(authorized_agent.id)
        assert agent.id == authorized_agent.id

