from src.api.configs.config import Config
import requests as http_requests
from src.api.models.comparison.model_assertions import ModelAssertions
from src.api.models.requests import CreateProjectRequest
from src.api.models.responses import ProjectsListResponse, ProjectResponse
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.base_steps import BaseSteps


class ProjectSteps(BaseSteps):
    def get_projects(self) -> ProjectsListResponse:
        projects: ProjectsListResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_PROJECTS,
            ResponseSpecs.request_return_ok(),
        ).get()

        assert projects.count >= 1
        return projects

    def get_projects_unauthorized(self):
        CrudRequester(
            request_spec=RequestSpecs.unauth_spec(),
            endpoint=Endpoint.GET_PROJECTS,
            response_spec=ResponseSpecs.request_return_unauth(),
        ).get()

    def get_project_by_id(self, project_id: str) -> ProjectResponse:
        project: ProjectResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_PROJECT,
            ResponseSpecs.request_return_ok(),
        ).get(locator=project_id)

        assert project.id == project_id
        return project

    def create_project(self, create_project_request: CreateProjectRequest) -> ProjectResponse:
        project: ProjectResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.CREATE_PROJECT,
            ResponseSpecs.request_return_ok(),
        ).post(create_project_request)
        self.created_objects.append(project)

        ModelAssertions(create_project_request, project).match()
        return project

    def delete_project(self, locator: str):
        ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.DELETE_PROJECT,
            ResponseSpecs.entity_was_deleted(),
        ).delete(locator)
        # Убираем из списка, чтобы cleanup не пытался удалить повторно
        self.created_objects[:] = [
            obj for obj in self.created_objects
            if not (isinstance(obj, ProjectResponse) and obj.id == locator)
        ]

    def get_deleted_project(self, locator: str):
        CrudRequester(
            request_spec=RequestSpecs.admin_base_headers(),
            endpoint=Endpoint.GET_PROJECTS,
            response_spec=ResponseSpecs.entity_was_not_found(),
        ).get(locator=locator)

    def archive_project(self, project_id: str, archived: bool):
        headers = dict(RequestSpecs.admin_base_headers())
        headers["Content-Type"] = "text/plain"
        headers["Accept"] = "text/plain"
        response = http_requests.put(
            url=f"{Config.get('baseurl')}projects/id:{project_id}/archived",
            data=str(archived).lower(),
            headers=headers,
        )
        ResponseSpecs.request_return_ok()(response)
