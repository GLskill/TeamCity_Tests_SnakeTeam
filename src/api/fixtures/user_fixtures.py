import pytest
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import CreateUserRequest


@pytest.fixture()
def user_request() -> CreateUserRequest:
    return RandomModelGenerator.generate(CreateUserRequest)


@pytest.fixture()
def created_user(user_request, api_manager):
    return api_manager.user_steps.admin_create_user(user_request)
