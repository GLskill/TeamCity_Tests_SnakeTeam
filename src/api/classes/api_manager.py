from src.api.specs.request_spec import RequestSpecs
from src.api.steps.agent_steps import AgentSteps
from src.api.steps.build_steps import BuildSteps
from src.api.steps.project_steps import ProjectSteps
from src.api.steps.server_steps import ServerSteps
from src.api.steps.super_user_steps import SuperUserSteps
from src.api.steps.vcsroot_steps import VcsRootSteps
from src.api.steps.user_steps import AdminUserSteps


class ApiManager:
    def __init__(self, created_objects: list, token: str = None):
        headers = RequestSpecs.token_auth_headers(token) if token else None
        self.build_steps: BuildSteps = BuildSteps(created_objects, headers)
        self.project_steps: ProjectSteps = ProjectSteps(created_objects, headers)
        self.agent_steps: AgentSteps = AgentSteps(created_objects, headers)
        self.vcsroot_steps: VcsRootSteps = VcsRootSteps(created_objects, headers)
        self.user_steps: AdminUserSteps = AdminUserSteps(created_objects, headers)
        self.super_user_steps: SuperUserSteps = SuperUserSteps(created_objects)
        self.server_steps: ServerSteps = ServerSteps(created_objects, headers)
