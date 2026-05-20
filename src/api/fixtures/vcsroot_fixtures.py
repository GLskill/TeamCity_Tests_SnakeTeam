import pytest

from src.api.generators.data_factory import make_vcs_root_request
from src.api.models.requests import CreateVcsRootRequest


@pytest.fixture()
def vcs_root_request(created_project) -> CreateVcsRootRequest:
    return make_vcs_root_request(created_project)
