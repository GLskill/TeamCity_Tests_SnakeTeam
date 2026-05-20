import os

from src.api.models.responses import ServerInfoResponse, CurrentUserResponse
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.base_steps import BaseSteps


class ServerSteps(BaseSteps):
    def get_server_info(self) -> ServerInfoResponse:
        server_info: ServerInfoResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_SERVER_INFO,
            ResponseSpecs.request_return_ok(),
        ).get()

        assert server_info.version is not None
        return server_info

    def get_current_user(self) -> CurrentUserResponse:
        user: CurrentUserResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_CURRENT_USER,
            ResponseSpecs.request_return_ok(),
        ).get()

        assert user.username == os.getenv('TC_ADMIN_USERNAME')
        return user

    def get_current_user_unauthorized(self):
        CrudRequester(
            request_spec=RequestSpecs.unauth_spec(),
            endpoint=Endpoint.GET_CURRENT_USER,
            response_spec=ResponseSpecs.request_return_unauth(),
        ).get()
