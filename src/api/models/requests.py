from typing import Annotated, Optional

from pydantic import Field

from src.api.generators.generating_rule import GeneratingRule
from src.api.models.base_model import BaseModel


class ParentProject(BaseModel):
    locator: str = '_Root'


class CreateProjectRequest(BaseModel):
    id: Annotated[str, GeneratingRule(regex=r"^ProjectId_[a-z0-9]{4}$")]
    name: Annotated[str, GeneratingRule(regex=r"^ProjectName_[a-z0-9]{4}$")]
    parentProject: Annotated[ParentProject, GeneratingRule(skip=True)] = ParentProject()


class ProjectRef(BaseModel):
    id: str


class CreateBuildTypeRequest(BaseModel):
    id: Annotated[str, GeneratingRule(regex=r"^BuildTypeId_[a-z0-9]{4}$")]
    name: Annotated[str, GeneratingRule(regex=r"^BuildTypeName_[a-z0-9]{4}$")]
    project: ProjectRef = Field(default=None)


class BuildTypeRef(BaseModel):
    id: str


class Comment(BaseModel):
    text: Optional[str] = None


class Agent(BaseModel):
    id: Optional[int] = None


class QueueBuildRequest(BaseModel):
    buildType: BuildTypeRef
    branchName: Optional[str] = None
    comment: Optional[Comment] = None
    agent: Optional[Agent] = None
    personal: Optional[bool] = None


class CopyBuildTypeRequest(BaseModel):
    sourceBuildTypeLocator: str
    name: str
    id: str
    copyAllAssociatedSettings: bool = True


class VcsRootProjectRef(BaseModel):
    id: str


class VcsRootProperty(BaseModel):
    name: str
    value: str


class VcsRootProperties(BaseModel):
    property: list[VcsRootProperty]


class CreateVcsRootRequest(BaseModel):
    id: str
    name: str
    vcsName: str
    project: VcsRootProjectRef
    properties: VcsRootProperties


class BuildCancelRequest(BaseModel):
    comment: str
    readdIntoQueue: bool


class GroupRef(BaseModel):
    key: str


class GroupsUpdateRequest(BaseModel):
    group: list[GroupRef]


class RoleRef(BaseModel):
    roleId: str
    scope: str


class RolesUpdateRequest(BaseModel):
    role: list[RoleRef]


class CreateUserRequest(BaseModel):
    username: Annotated[str, GeneratingRule(regex=r"^[A-Za-z][A-Za-z0-9]{3,10}$")]
    password: Annotated[str, GeneratingRule(regex=r"^[A-Z]{2}[a-z]{3}[0-9]{2}[!@#]{1}$")]
    email: Annotated[Optional[str], GeneratingRule(skip=True)] = None
    name: Annotated[Optional[str], GeneratingRule(skip=True)] = None