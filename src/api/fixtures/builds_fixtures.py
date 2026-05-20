import pytest

from src.enums import BuildComment, VcsRootParams
from src.api.generators.data_factory import make_copy_build_request
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import BuildCancelRequest, Agent, Comment
from src.api.models.responses import QueueBuildResponse, BuildTypeResponse
from src.api.models.requests import CreateBuildTypeRequest, ProjectRef, QueueBuildRequest, BuildTypeRef, \
    CopyBuildTypeRequest
from src.api.steps.build_steps import BuildSteps


@pytest.fixture()
def build_steps(api_manager) -> BuildSteps:
    return api_manager.build_steps


@pytest.fixture()
def build_type_request(created_project) -> CreateBuildTypeRequest:
    build_type_data: CreateBuildTypeRequest = RandomModelGenerator.generate(CreateBuildTypeRequest)
    build_type_data.project = ProjectRef(id=created_project.id)
    return build_type_data


@pytest.fixture()
def build_type(build_type_request, api_manager) -> BuildTypeResponse:
    return api_manager.build_steps.create_build_type(build_type_request)


@pytest.fixture()
def queue_build_request(build_type) -> QueueBuildRequest:
    return QueueBuildRequest(buildType=BuildTypeRef(id=build_type.id))


@pytest.fixture()
def queue_build(queue_build_request, api_manager) -> QueueBuildResponse:
    return api_manager.build_steps.add_build_to_queue(queue_build_request)


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
def sub_build_type(api_manager, sub_project):
    build_data = RandomModelGenerator.generate(CreateBuildTypeRequest)
    build_data.project = ProjectRef(id=sub_project.id)
    return api_manager.build_steps.create_build_type(build_data)


@pytest.fixture()
def custom_build_request(build_type, get_enable_agent) -> QueueBuildRequest:
    return QueueBuildRequest(
        buildType=BuildTypeRef(id=build_type.id),
        branchName=VcsRootParams.BRANCH_VALUE,
        agent=Agent(id=get_enable_agent.id),
        comment=Comment(text=BuildComment.CUSTOM_BUILD),
        personal=False
    )