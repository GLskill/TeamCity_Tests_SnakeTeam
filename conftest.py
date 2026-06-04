from src.api.fixtures.project_fixtures import *
from src.api.fixtures.builds_fixtures import *
from src.api.fixtures.api_fixtures import *
from src.api.fixtures.object_cleanup_fixtures import *
from src.api.fixtures.agent_fixtures import *
from src.api.fixtures.vcsroot_fixtures import vcs_root_request
from src.api.fixtures.user_fixtures import *
from src.ui.fixtures.ui_system_admin_fixtures import *
from src.ui.fixtures.ui_base_fixures import *


@pytest.fixture(scope="session", autouse=True)
def disable_all_agents_before_session():
    from src.api.classes.api_manager import ApiManager
    manager = ApiManager([])
    agents = manager.agent_steps.get_authorized_agents()
    for agent in (agents.agent or []):
        try:
            manager.agent_steps.disable_agent(agent)
        except Exception:
            pass
    yield

