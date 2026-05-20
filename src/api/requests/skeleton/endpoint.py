from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.api.models.base_model import BaseModel
from src.api.models.requests import (CreateProjectRequest, CreateBuildTypeRequest, QueueBuildRequest, CopyBuildTypeRequest,
                                     CreateVcsRootRequest, BuildCancelRequest, RolesUpdateRequest, GroupsUpdateRequest,
                                     CreateUserRequest)
from src.api.models.responses import (ServerInfoResponse, CurrentUserResponse, ProjectResponse, ProjectsListResponse,
                                      BuildTypeResponse, QueueBuildResponse, AgentsListResponse, VcsRootResponse,
                                      AgentResponse, BuildTypesListResponse, UserResponse, TokenResponse,
                                      TokensListResponse, RolesListResponse, GroupsListResponse, UsersListResponse)


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: Optional[type[BaseModel]]
    response_model: Optional[type[BaseModel]]


class Endpoint(Enum):
    GET_SERVER_INFO = EndpointConfig(
        url='server',
        request_model=None,
        response_model=ServerInfoResponse,
    )

    GET_CURRENT_USER = EndpointConfig(
        url='users/current',
        request_model=None,
        response_model=CurrentUserResponse,
    )

    GET_PROJECTS = EndpointConfig(
        url='projects',
        request_model=None,
        response_model=ProjectsListResponse,
    )

    GET_PROJECT = EndpointConfig(
        url='projects',
        request_model=None,
        response_model=ProjectResponse,
    )

    CREATE_PROJECT = EndpointConfig(
        url='projects',
        request_model=CreateProjectRequest,
        response_model=ProjectResponse,
    )

    DELETE_PROJECT = EndpointConfig(
        url='projects',
        request_model=None,
        response_model=None,
    )

    CREATE_BUILD_TYPE = EndpointConfig(
        url='buildTypes',
        request_model=CreateBuildTypeRequest,
        response_model=BuildTypeResponse,
    )

    DELETE_BUILD_TYPE = EndpointConfig(
        url='buildTypes',
        request_model=None,
        response_model=None,
    )

    GET_BUILD_TYPE = EndpointConfig(
        url='buildTypes',
        request_model=None,
        response_model=BuildTypeResponse,
    )

    QUEUE_BUILD = EndpointConfig(
        url='buildQueue',
        request_model=QueueBuildRequest,
        response_model=QueueBuildResponse,
    )

    GET_QUEUED_BUILD = EndpointConfig(
        url='buildQueue',
        request_model=None,
        response_model=QueueBuildResponse,
    )

    GET_LIST_AGENTS = EndpointConfig(
        url='agents',
        request_model=None,
        response_model=AgentsListResponse,
    )

    GET_AGENT = EndpointConfig(
        url='agents',
        request_model=None,
        response_model=AgentResponse,
    )

    COPY_BUILD_TYPE_TO_PROJECT = EndpointConfig(
        url='projects',
        request_model=CopyBuildTypeRequest,
        response_model=BuildTypeResponse,
    )

    GET_BUILD_TYPES_BY_PROJECT = EndpointConfig(
        url='buildTypes',
        request_model=None,
        response_model=BuildTypesListResponse,
    )

    MOVE_BUILD_TYPE = EndpointConfig(
        url='buildTypes',
        request_model=None,
        response_model=BuildTypeResponse,
    )

    CREATE_VCS_ROOT = EndpointConfig(
        url='vcs-roots',
        request_model=CreateVcsRootRequest,
        response_model=VcsRootResponse,
    )

    GET_VCS_ROOT = EndpointConfig(
        url='vcs-roots',
        request_model=None,
        response_model=VcsRootResponse,
    )

    DELETE_VCS_ROOT = EndpointConfig(
        url='vcs-roots',
        request_model=None,
        response_model=None,
    )

    CANCEL_QUEUED_BUILD = EndpointConfig(
        url='buildQueue',
        request_model=BuildCancelRequest,
        response_model=QueueBuildResponse,
    )

    CANCEL_RUNNING_BUILD = EndpointConfig(
        url='builds',
        request_model=BuildCancelRequest,
        response_model=QueueBuildResponse,
    )

    CREATE_USER = EndpointConfig(
        url='users',
        request_model=CreateUserRequest,
        response_model=UserResponse,
    )

    GET_USER = EndpointConfig(
        url='users',
        request_model=None,
        response_model=UserResponse,
    )

    GET_USERS = EndpointConfig(
        url='users',
        request_model=None,
        response_model=UsersListResponse,
    )

    GET_USER_GROUPS = EndpointConfig(
        url='users',
        request_model=None,
        response_model=GroupsListResponse,
    )

    UPDATE_USER_GROUPS = EndpointConfig(
        url='users',
        request_model=GroupsUpdateRequest,
        response_model=GroupsListResponse,
    )

    DELETE_USER = EndpointConfig(
        url='users',
        request_model=None,
        response_model=None,
    )

    DELETE_USER_FROM_GROUP = EndpointConfig(
        url='users',
        request_model=None,
        response_model=None,
    )

    GET_USER_ROLES = EndpointConfig(
        url='users',
        request_model=None,
        response_model=RolesListResponse,
    )

    UPDATE_USER_ROLES = EndpointConfig(
        url='users',
        request_model=RolesUpdateRequest,
        response_model=RolesListResponse,
    )

    DELETE_USER_ROLE = EndpointConfig(
        url='users',
        request_model=None,
        response_model=None,
    )

    GET_USER_TOKENS = EndpointConfig(
        url='users',
        request_model=None,
        response_model=TokensListResponse,
    )

    CREATE_USER_TOKEN = EndpointConfig(
        url='users',
        request_model=None,
        response_model=TokenResponse,
    )

    DELETE_USER_TOKEN = EndpointConfig(
        url='users',
        request_model=None,
        response_model=None,
    )
