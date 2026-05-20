from src.api.models.requests import GroupsUpdateRequest, GroupRef, RolesUpdateRequest, RoleRef, CreateUserRequest
from src.api.models.responses import (
    UserResponse, UsersListResponse, GroupsListResponse,
    RolesListResponse, TokensListResponse, TokenResponse, CurrentUserResponse,
)
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.base_steps import BaseSteps
from requests import Response


class AdminUserSteps(BaseSteps):
    def admin_create_user(self, create_user_request: CreateUserRequest) -> UserResponse:
        user: UserResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.CREATE_USER,
            ResponseSpecs.request_return_ok(),
        ).post(create_user_request)
        self.created_objects.append(user)
        return user

    def admin_create_invalid_user(self, create_user_request: CreateUserRequest, error_key: str, error_value: str):
        CrudRequester(
            request_spec=RequestSpecs.admin_base_headers(),
            endpoint=Endpoint.CREATE_USER,
            response_spec=ResponseSpecs.request_return_bad_request(error_key, error_value),
        ).post(create_user_request)

    def admin_get_all_users(self) -> list:
        users: UsersListResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_USERS,
            ResponseSpecs.request_return_ok(),
        ).get()
        return users.user or []

    def admin_get_user_by_id(self, user_id: int) -> UserResponse:
        user: UserResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_USER,
            ResponseSpecs.request_return_ok(),
        ).get(locator=f'id:{user_id}')
        assert user.id == user_id
        return user

    def admin_get_user_by_username(self, username: str) -> UserResponse:
        user: UserResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_USER,
            ResponseSpecs.request_return_ok(),
        ).get(locator=f'username:{username}')
        assert user.username == username
        return user

    def admin_get_current_user(self) -> CurrentUserResponse:
        current: CurrentUserResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_CURRENT_USER,
            ResponseSpecs.request_return_ok(),
        ).get()
        return current

    def admin_delete_user(self, user_id: int) -> None:
        ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.DELETE_USER,
            ResponseSpecs.entity_was_deleted(),
        ).delete(locator=f'id:{user_id}')
        self.created_objects[:] = [
            obj for obj in self.created_objects
            if not (isinstance(obj, UserResponse) and obj.id == user_id)
        ]

    def admin_get_deleted_user(self, user_id: int) -> None:
        CrudRequester(
            request_spec=RequestSpecs.admin_base_headers(),
            endpoint=Endpoint.GET_USER,
            response_spec=ResponseSpecs.entity_was_not_found(),
        ).get(locator=f'id:{user_id}')

    def admin_get_user_groups(self, user_id: int) -> list:
        groups: GroupsListResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_USER_GROUPS,
            ResponseSpecs.request_return_ok(),
        ).get(locator=f'id:{user_id}/groups')
        return groups.group or []

    def admin_update_user_groups(self, user_id: int, group_keys: list[str]) -> list:
        body = GroupsUpdateRequest(group=[GroupRef(key=k) for k in group_keys])
        groups: GroupsListResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.UPDATE_USER_GROUPS,
            ResponseSpecs.request_return_ok(),
        ).put(locator=f'id:{user_id}/groups', body=body)
        return groups.group or []

    def admin_remove_user_from_group(self, user_id: int, group_locator: str) -> None:
        ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.DELETE_USER_FROM_GROUP,
            ResponseSpecs.entity_was_deleted(),
        ).delete(locator=f'id:{user_id}/groups/{group_locator}')

    def admin_get_user_roles(self, user_id: int) -> list:
        roles: RolesListResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_USER_ROLES,
            ResponseSpecs.request_return_ok(),
        ).get(locator=f'id:{user_id}/roles')
        return roles.role or []

    def admin_update_user_roles(self, user_id: int, role_id: str, scope: str) -> list:
        body = RolesUpdateRequest(role=[RoleRef(roleId=role_id, scope=scope)])
        roles: RolesListResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.UPDATE_USER_ROLES,
            ResponseSpecs.request_return_ok(),
        ).put(locator=f'id:{user_id}/roles', body=body)
        return roles.role or []

    def admin_remove_user_role(self, user_id: int, role_id: str, scope: str) -> None:
        ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.DELETE_USER_ROLE,
            ResponseSpecs.entity_was_deleted(),
        ).delete(locator=f'id:{user_id}/roles/{role_id}/{scope}')

    def admin_get_user_tokens(self, user_id: int) -> list:
        tokens: TokensListResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.GET_USER_TOKENS,
            ResponseSpecs.request_return_ok(),
        ).get(locator=f'id:{user_id}/tokens')
        return tokens.token or []

    def admin_create_user_token(self, user_id: int, token_name: str) -> TokenResponse:
        token: TokenResponse = ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.CREATE_USER_TOKEN,
            ResponseSpecs.request_return_ok(),
        ).post(locator=f'id:{user_id}/tokens/{token_name}')
        return token

    def admin_create_user_token_raw(self, user_id: int, token_name: str) -> Response:
        return CrudRequester(
            request_spec=RequestSpecs.admin_base_headers(),
            endpoint=Endpoint.CREATE_USER_TOKEN,
            response_spec=lambda r: r,
        ).post(model=None, locator=f'id:{user_id}/tokens/{token_name}')

    def admin_delete_user_token(self, user_id: int, token_name: str) -> None:
        ValidatedCrudRequester(
            RequestSpecs.admin_base_headers(),
            Endpoint.DELETE_USER_TOKEN,
            ResponseSpecs.entity_was_deleted(),
        ).delete(locator=f'id:{user_id}/tokens/{token_name}')

    def admin_delete_user_token_raw(self, user_id: int, token_name: str) -> Response:
        return CrudRequester(
            request_spec=RequestSpecs.admin_base_headers(),
            endpoint=Endpoint.DELETE_USER_TOKEN,
            response_spec=lambda r: r,
        ).delete(locator=f'id:{user_id}/tokens/{token_name}')
