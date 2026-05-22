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
    snapshot = list(objects)  # копия списка, чтобы delete_project не ломал итерацию
    print(f"\n[CLEANUP] objects to clean: {snapshot}")
    api_manager = ApiManager(objects)

    for obj in snapshot:   # 1) VCS Roots
        if isinstance(obj, VcsRootResponse):
            try:
                api_manager.vcsroot_steps.delete_vcs_root(obj.id)
            except Exception:
                pass

    for obj in snapshot:  # 2) BuildTypes
        if isinstance(obj, BuildTypeResponse):
            try:
                api_manager.build_steps.delete_build_type(obj.id)
            except Exception:
                pass

    for obj in snapshot:   # 3) Projects
        if isinstance(obj, ProjectResponse):
            try:
                print(f"[CLEANUP] Deleting project: {obj.id}")
                api_manager.project_steps.delete_project(obj.id)
                print(f"[CLEANUP] Deleted OK: {obj.id}")
            except Exception as e:
                logging.warning(f"[CLEANUP] Failed to delete project {obj.id}: {e}")

    for obj in snapshot:   # 4) Users
        if isinstance(obj, UserResponse):
            try:
                api_manager.user_steps.admin_delete_user(obj.id)
            except Exception:
                pass

    for obj in snapshot:   # 5) Agents — выключаем (enable_agent добавляет в created_objects)
        if isinstance(obj, AgentResponse):
            try:
                api_manager.agent_steps.disable_agent(obj)
            except Exception:
                pass
            # Деавторизацию не делаем здесь намеренно:
            # authorized_agent фикстура сама управляет авторизацией через yield-teardown.
            # Если деавторизовывать здесь — будет двойной вызов и возможная ошибка 404.

    known_types = (VcsRootResponse, BuildTypeResponse, ProjectResponse, UserResponse, AgentResponse)
    for obj in snapshot:   # 6) Неизвестные типы
        if not isinstance(obj, known_types):
            logging.warning(f'Cleanup is not implemented for object type: {type(obj)}')