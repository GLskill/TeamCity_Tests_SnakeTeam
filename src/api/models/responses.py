from src.api.models.base_model import BaseModel
from typing import Optional


class ServerInfoResponse(BaseModel):
    version: str
    buildDate: Optional[str] = None
    buildNumber: Optional[str] = None


class CurrentUserResponse(BaseModel):
    username: str
    id: Optional[int] = None
    name: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    archived: Optional[bool] = None
    parentProjectId: Optional[str] = None


class ProjectsListResponse(BaseModel):
    count: int
    project: Optional[list] = None


class BuildTypeResponse(BaseModel):
    id: str
    name: str
    project: Optional[dict] = None
    paused: Optional[bool] = None


class BuildTypesListResponse(BaseModel):
    count: int
    buildType: Optional[list[BuildTypeResponse]] = None

    def get_ids(self) -> list[str]:
        return [bt.id for bt in self.buildType or []]


class Comment(BaseModel):
    text: Optional[str] = None


class QueueBuildResponse(BaseModel):
    id: int
    state: str
    buildType: Optional[dict] = None
    status: Optional[str] = None
    comment: Optional[Comment] = None
    canceledInfo: Optional[Comment] = None


class AgentResponse(BaseModel):
    id: int
    name: str
    connected: Optional[bool] = None
    enabled: Optional[bool] = None
    authorized: Optional[bool] = None


class AgentsListResponse(BaseModel):
    count: int
    agent: list[AgentResponse]


class VcsRootResponse(BaseModel):
    id: str
    name: str
    vcsName: Optional[str] = None
    project: Optional[dict] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    name: Optional[str] = None


class UsersListResponse(BaseModel):
    count: int
    user: Optional[list] = None


class TokenResponse(BaseModel):
    name: str
    value: Optional[str] = None
    creationTime: Optional[str] = None


class TokensListResponse(BaseModel):
    count: int
    token: Optional[list[TokenResponse]] = None


class RoleResponse(BaseModel):
    roleId: str
    scope: Optional[str] = None
    href: Optional[str] = None


class RolesListResponse(BaseModel):
    role: Optional[list[RoleResponse]] = None


class GroupResponse(BaseModel):
    key: str
    name: Optional[str] = None
    href: Optional[str] = None


class GroupsListResponse(BaseModel):
    count: int
    group: Optional[list[GroupResponse]] = None
