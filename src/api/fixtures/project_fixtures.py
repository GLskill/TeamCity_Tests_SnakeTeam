import pytest

from src.api.generators.data_factory import make_sub_project_request
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import CreateProjectRequest
from src.api.models.responses import ProjectResponse
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.project_steps import ProjectSteps


@pytest.fixture()
def project_steps(api_manager) -> ProjectSteps:
    return api_manager.project_steps


@pytest.fixture()
def get_project_request():
    project_data: CreateProjectRequest = RandomModelGenerator.generate(CreateProjectRequest)
    return project_data


@pytest.fixture()
def created_project(get_project_request, api_manager):
    project = api_manager.project_steps.create_project(get_project_request)
    return project


@pytest.fixture()
def project_not_found():
    return CrudRequester(
        request_spec=RequestSpecs.admin_base_headers(),
        endpoint=Endpoint.GET_PROJECTS,
        response_spec=ResponseSpecs.entity_was_not_found()
    )


@pytest.fixture()
def archive_project(api_manager):
    return api_manager.project_steps.archive_project


@pytest.fixture()
def sub_project(api_manager, created_project):
    return api_manager.project_steps.create_project(make_sub_project_request(created_project))


@pytest.fixture()
def sub_project_request(created_project) -> CreateProjectRequest:
    return make_sub_project_request(created_project)


@pytest.fixture()
def target_project(api_manager, created_objects) -> ProjectResponse:
    project_data = RandomModelGenerator.generate(CreateProjectRequest)
    project = api_manager.project_steps.create_project(project_data)
    created_objects.append(project)
    return project
