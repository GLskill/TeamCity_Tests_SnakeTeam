from src.api.models.responses import UserResponse, TokenResponse
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.base_steps import BaseSteps
from src.enums import UiFirstUp


class PreAdminSteps(BaseSteps):

    def setup_create_token(self, token_name: str) -> str:
        """Создаёт токен через Basic Auth — используется только в set_up.py."""
        user: UserResponse = ValidatedCrudRequester(
            RequestSpecs.admin_basic_auth_headers(),
            Endpoint.GET_USER,
            ResponseSpecs.request_return_ok(),
        ).get(locator=f'username:{UiFirstUp.ADMIN_USERNAME}')

        # Удаляем старый токен если есть (идемпотентность)
        CrudRequester(
            request_spec=RequestSpecs.admin_basic_auth_headers(),
            endpoint=Endpoint.DELETE_USER_TOKEN,
            response_spec=lambda r: r,
        ).delete(locator=f'id:{user.id}/tokens/{token_name}')

        token: TokenResponse = ValidatedCrudRequester(
            RequestSpecs.admin_basic_auth_headers(),
            Endpoint.CREATE_USER_TOKEN,
            ResponseSpecs.request_return_ok(),
        ).post(locator=f'id:{user.id}/tokens/{token_name}')

        return token.value