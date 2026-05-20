import logging
from typing import Any, List
import pytest
from src.api.models.responses import UserResponse, VcsRootResponse
from src.api.classes.api_manager import ApiManager
from src.api.models.responses import ProjectResponse, BuildTypeResponse, AgentResponse


@pytest.fixture
def created_objects():
    objects: List[Any] = []
    yield objects

    cleanup_objects(objects)


def cleanup_objects(objects: List[Any]):    # Важно: порядок удаления имеет значение.
    api_manager = ApiManager(objects)

    for obj in objects:   # 1) VCS Roots
        if isinstance(obj, VcsRootResponse):
            try:
                api_manager.vcsroot_steps.delete_vcs_root(obj.id)
            except Exception:
                pass

    for obj in objects:  # 2) BuildTypes
        if isinstance(obj, BuildTypeResponse):
            try:
                api_manager.build_steps.delete_build_type(obj.id)
            except Exception:
                pass

    for obj in objects:   # 3) Projects
        if isinstance(obj, ProjectResponse):
            try:
                api_manager.project_steps.delete_project(obj.id)
            except Exception:
                pass

    for obj in objects:   # 4) Users
        if isinstance(obj, UserResponse):
            try:
                api_manager.user_steps.admin_delete_user(obj.id)
            except Exception:
                pass

    for obj in objects:   # 5) Agents
        if isinstance(obj, AgentResponse):
            try:
                api_manager.agent_steps.disable_agent(obj)
            except Exception:
                pass

    known_types = (VcsRootResponse, BuildTypeResponse, ProjectResponse, UserResponse, AgentResponse)
    for obj in objects:   # 6) Неизвестные типы
        if not isinstance(obj, known_types):
            logging.warning(f'Cleanup is not implemented for object type: {type(obj)}')
