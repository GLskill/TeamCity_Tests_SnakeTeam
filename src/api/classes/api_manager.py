from src.api.steps.agent_steps import AgentSteps
from src.api.steps.build_steps import BuildSteps
from src.api.steps.project_steps import ProjectSteps
from src.api.steps.server_steps import ServerSteps
from src.api.steps.vcsroot_steps import VcsRootSteps
from src.api.steps.user_steps import AdminUserSteps


class ApiManager:
    def __init__(self, created_objects: list):
        self.build_steps: BuildSteps = BuildSteps(created_objects)
        self.project_steps: ProjectSteps = ProjectSteps(created_objects)
        self.agent_steps: AgentSteps = AgentSteps(created_objects)
        self.vcsroot_steps: VcsRootSteps = VcsRootSteps(created_objects)
        self.user_steps: AdminUserSteps = AdminUserSteps(created_objects)
        self.server_steps: ServerSteps = ServerSteps()
