import pytest

from src.api.classes.api_manager import ApiManager
from src.api.fixtures.api_fixtures import api_manager
from src.api.models.responses import AgentResponse


@pytest.fixture()
def get_disable_agent(api_manager) -> AgentResponse:
    agents = api_manager.agent_steps.get_disabled_agents()
    return agents.agent[0]


@pytest.fixture()
def enable_agent(get_disable_agent: AgentResponse, api_manager: ApiManager) -> None:
    api_manager.agent_steps.enable_agent(get_disable_agent)


@pytest.fixture()
def get_enable_agent(api_manager, enable_agent) -> AgentResponse:
    agents = api_manager.agent_steps.get_enabled_agents()
    return agents.agent[0]
