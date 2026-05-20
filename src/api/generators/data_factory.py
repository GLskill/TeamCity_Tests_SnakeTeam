from src.enums import VcsRootParams, BuildParams
from src.api.generators.random_data import RandomData
from src.api.generators.random_model_generator import RandomModelGenerator
from src.api.models.requests import (
    ParentProject, CreateVcsRootRequest, VcsRootProjectRef,
    VcsRootProperties, VcsRootProperty, CopyBuildTypeRequest, CreateBuildTypeRequest, CreateProjectRequest
)


def make_sub_project_request(created_project) -> CreateProjectRequest:
    project_data = RandomModelGenerator.generate(CreateProjectRequest)
    project_data.parentProject = ParentProject(locator=f'id:{created_project.id}')
    return project_data


def make_vcs_root_request(created_project) -> CreateVcsRootRequest:
    uid = RandomData.get_name()
    return CreateVcsRootRequest(
        id=f'{created_project.id}_Root{uid}',
        name=f'VcsRoot_{uid}',
        vcsName=VcsRootParams.VCS_NAME,
        project=VcsRootProjectRef(id=created_project.id),
        properties=VcsRootProperties(
            property=[VcsRootProperty(**p) for p in VcsRootParams.DEFAULT_PROPERTIES]
        )
    )


def make_copy_build_request(build_type_request: CreateBuildTypeRequest) -> CopyBuildTypeRequest:
    uid = RandomData.get_name()
    return CopyBuildTypeRequest(
        sourceBuildTypeLocator=f'id:{build_type_request.id}',
        name=f'{BuildParams.COPY_NAME_PREFIX} {uid}',
        id=f'{build_type_request.id}{BuildParams.COPY_ID_SUFFIX}{uid}',
        copyAllAssociatedSettings=True,
    )
