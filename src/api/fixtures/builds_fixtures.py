import pytest

from src.enums import BuildComment, VcsRootParams
from src.api.generators.data_factory import make_copy_build_request
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import BuildCancelRequest, Agent, Comment
from src.api.models.responses import QueueBuildResponse, BuildTypeResponse, AgentResponse
from src.api.models.requests import CreateBuildTypeRequest, ProjectRef, QueueBuildRequest, BuildTypeRef, \
    CopyBuildTypeRequest


@pytest.fixture()
def build_type_request(created_project) -> CreateBuildTypeRequest:
    build_type_data: CreateBuildTypeRequest = RandomModelGenerator.generate(CreateBuildTypeRequest)
    build_type_data.project = ProjectRef(id=created_project.id)
    return build_type_data


@pytest.fixture()
def build_type(build_type_request, admin_api_manager) -> BuildTypeResponse:
    return admin_api_manager.build_steps.create_build_type(build_type_request)


@pytest.fixture()
def running_build_type(build_type, admin_api_manager) -> BuildTypeResponse:
    admin_api_manager.build_steps.add_sleep_command_line_step(build_type.id)
    return build_type


@pytest.fixture()
def queue_build_request(build_type) -> QueueBuildRequest:
    return QueueBuildRequest(buildType=BuildTypeRef(id=build_type.id))


@pytest.fixture()
def queue_build(queue_build_request, admin_api_manager) -> QueueBuildResponse:
    return admin_api_manager.build_steps.add_build_to_queue(queue_build_request)


@pytest.fixture()
def running_queue_build_request(running_build_type, connected_authorized_agent: AgentResponse) -> QueueBuildRequest:
    return QueueBuildRequest(
        buildType=BuildTypeRef(id=running_build_type.id),
        agent=Agent(id=connected_authorized_agent.id),
        personal=False
    )


@pytest.fixture()
def running_queue_build(running_queue_build_request, admin_api_manager) -> QueueBuildResponse:
    return admin_api_manager.build_steps.add_build_to_queue(running_queue_build_request)


@pytest.fixture()
def queued_build_cancel_request() -> BuildCancelRequest:
    return BuildCancelRequest(comment=BuildComment.CANCELING_QUEUED_BUILD, readdIntoQueue=False)


@pytest.fixture()
def running_build_cancel_request() -> BuildCancelRequest:
    return BuildCancelRequest(comment=BuildComment.CANCELING_RUNNING_BUILD, readdIntoQueue=False)


@pytest.fixture()
def copy_build_request(build_type_request) -> CopyBuildTypeRequest:
    return make_copy_build_request(build_type_request)


@pytest.fixture()
def sub_build_type(admin_api_manager, sub_project):
    build_data = RandomModelGenerator.generate(CreateBuildTypeRequest)
    build_data.project = ProjectRef(id=sub_project.id)
    return admin_api_manager.build_steps.create_build_type(build_data)


@pytest.fixture()
def custom_build_request(build_type, authorized_agent: AgentResponse) -> QueueBuildRequest:
    return QueueBuildRequest(
        buildType=BuildTypeRef(id=build_type.id),
        branchName=VcsRootParams.BRANCH_VALUE,
        agent=Agent(id=authorized_agent.id),
        comment=Comment(text=BuildComment.CUSTOM_BUILD),
        personal=False
    )
