from src.api.models.requests import CreateUserRequest, RolesUpdateRequest, RoleRef
from src.api.models.responses import UserResponse
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs
from src.api.steps.base_steps import BaseSteps


class SuperUserSteps(BaseSteps):
    def create_system_admin(self, create_user_request: CreateUserRequest) -> UserResponse:
        # Шаг 1: создаём пользователя
        user: UserResponse = ValidatedCrudRequester(
            RequestSpecs.super_user_headers(),
            Endpoint.CREATE_USER,
            ResponseSpecs.request_return_ok(),
        ).post(create_user_request)

        # Шаг 2: назначаем роль SYSTEM_ADMIN глобально
        roles_payload = RolesUpdateRequest(
            role=[RoleRef(roleId="SYSTEM_ADMIN", scope="g")]
        )
        ValidatedCrudRequester(
            RequestSpecs.super_user_headers(),
            Endpoint.UPDATE_USER_ROLES,
            ResponseSpecs.request_return_ok(),
        ).put(f'id:{user.id}/roles', roles_payload)
        self.created_objects.append(user)
        return user

    def delete_system_admin(self, user_id: int) -> None:
        ValidatedCrudRequester(
            RequestSpecs.super_user_headers(),
            Endpoint.DELETE_USER,
            ResponseSpecs.entity_was_deleted(),
        ).delete(f'id:{user_id}')

        self.created_objects[:] = [
            obj for obj in self.created_objects
            if not (isinstance(obj, UserResponse) and obj.id == user_id)
        ]
