from enum import StrEnum


class BuildState(StrEnum):
    QUEUED = 'queued'
    FINISHED = 'finished'
    RUNNING = 'running'
    DELETED = 'deleted'
    UNKNOWN = 'unknown'


class BuildComment(StrEnum):
    CANCELING_QUEUED_BUILD = 'Canceling a queued build'
    CANCELING_RUNNING_BUILD = 'Canceling a running build'
    CUSTOM_BUILD = 'Start Custom Build'


class BuildStatus(StrEnum):
    NULL = 'null'  # for queued builds.
    SUCCESS = 'SUCCESS'  # for builds that have successfully finished or still running without errors.
    FAILURE = 'FAILURE'  # for builds that failed to start or failed during their run.
    UNKNOWN = 'UNKNOWN'  # for canceled builds.


class ContentType(StrEnum):
    TEXT_PLAIN = 'text/plain'
    APPLICATION_JSON = 'application/json'


class UserParams(StrEnum):
    NONEXISTENT_ID = '191919991919'


class UserTokenParams:
    MISSING_TOKEN_NAME = 'token-does-not-exist-123'
    CREATE_FORBIDDEN_STATUS = 403
    DELETE_MISSING_TOKEN_STATUSES = (400, 404)


class BuildParams(StrEnum):
    PARAM_NAME = 'env.SMOKE_PARAM'
    PARAM_VALUE = 'NEW_parameter'
    COPY_NAME_PREFIX = 'Copied Build'
    COPY_ID_SUFFIX = '_Copy'


class VcsRootParams:
    VCS_NAME = 'jetbrains.git'
    AUTH_METHOD_NAME = 'authMethod'
    AUTH_METHOD_VALUE = 'ADMIN'
    BRANCH_NAME = 'branch'
    BRANCH_VALUE = 'refs/heads/main'
    URL_NAME = 'url'
    URL_VALUE = 'https://github.com/JetBrains/teamcity-rest.git'
    DEFAULT_PROPERTIES = [
        {'name': 'authMethod', 'value': 'ANONYMOUS'},
        {'name': 'branch', 'value': 'refs/heads/main'},
        {'name': 'url', 'value': 'https://github.com/JetBrains/teamcity-rest.git'},
    ]


class UiAlert(StrEnum):
    INCORRECT_DATA = 'Incorrect username or password.'
    LOGIN_PAGE_VISIBLE = 'Log in to TeamCity'
    LOGIN_LIMIT_MSG = 'You made 5 failed login attempts in 1m.'
    NEW_PROJECT_TEXT = "New Project"
    CHANGES = 'Changes'
    ADMINISTRATION = 'Administration'
    AGENTS_OVERVIEW = 'Overview'
    AGENTS_FAVORITE_POOLS = 'Favorite Agent Pools'
    QUEUE = 'Builds in queue'
