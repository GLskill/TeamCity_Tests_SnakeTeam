import json

import allure
import requests as raw_requests

from src.api.configs.config import Config
from src.api.generators.random_data import RandomData
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import CreateUserRequest, RolesUpdateRequest, RoleRef
from src.api.models.responses import UserResponse
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.api.specs.request_spec import RequestSpecs
from src.api.specs.response_spec import ResponseSpecs


class AdminFactory:
    """Creates a fresh SYSTEM_ADMIN with a unique token for per-test isolation."""

    def create_admin_with_token(self, created_objects: list) -> tuple[UserResponse, str]:
        headers = RequestSpecs.super_user_headers()
        admin_request = RandomModelGenerator.generate(CreateUserRequest)
        token_name = f"test_{RandomData.get_name()}"

        with allure.step(f"[AdminFactory] Создать тестового admin: {admin_request.username}"):
            user: UserResponse = ValidatedCrudRequester(
                headers,
                Endpoint.CREATE_USER,
                ResponseSpecs.request_return_ok(),
            ).post(admin_request)

        with allure.step(f"[AdminFactory] Назначить роль SYSTEM_ADMIN → id:{user.id}"):
            ValidatedCrudRequester(
                headers,
                Endpoint.UPDATE_USER_ROLES,
                ResponseSpecs.request_return_ok(),
            ).put(f'id:{user.id}/roles', RolesUpdateRequest(role=[RoleRef(roleId="SYSTEM_ADMIN", scope="g")]))

        with allure.step(f"[AdminFactory] Создать токен '{token_name}' для {user.username}"):
            base = Config.get('baseurl').replace('/app/rest/', '').rstrip('/')
            response = raw_requests.post(
                f"{base}/httpAuth/app/rest/users/id:{user.id}/tokens/{token_name}",
                auth=(admin_request.username, admin_request.password),
                headers={'Accept': 'application/json'},
            )
            assert response.status_code == 200, f"Создание токена провалилось ({response.status_code}): {response.text}"
            personal_admin_token_value = response.json().get('value')
            assert personal_admin_token_value, "TC не вернул значение токена"

        allure.attach(
            json.dumps({
                "id": user.id,
                "username": user.username,
                "password": admin_request.password,
                "token_name": token_name,
                "token_value": personal_admin_token_value,
            }, indent=2, ensure_ascii=False),
            name="Test Admin Credentials",
            attachment_type=allure.attachment_type.JSON,
        )

        created_objects.append(user)
        return user, personal_admin_token_value
