import pytest

from src.api.classes.api_manager import ApiManager
from src.api.steps.admin_factory import AdminFactory


@pytest.fixture
def api_manager(created_objects) -> ApiManager:
    return ApiManager(created_objects)


@pytest.fixture
def admin_api_manager(created_objects) -> ApiManager:
    """ApiManager с уникальным per-test администратором и его токеном."""
    _, personal_admin_token = AdminFactory().create_admin_with_token(created_objects)
    return ApiManager(created_objects, token=personal_admin_token)
