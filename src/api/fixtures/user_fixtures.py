import allure
import pytest
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import CreateUserRequest


@pytest.fixture()
def user_request() -> CreateUserRequest:
    request = RandomModelGenerator.generate(CreateUserRequest)
    allure.attach(
        f"username: {request.username}\npassword: {request.password}",
        name="User credentials",
        attachment_type=allure.attachment_type.TEXT,
    )
    return request


@pytest.fixture()
def created_user(user_request, admin_api_manager):
    user = admin_api_manager.user_steps.admin_create_user(user_request)
    allure.attach(
        f"id: {user.id}\nusername: {user.username}",
        name="Created user",
        attachment_type=allure.attachment_type.TEXT,
    )
    return user
