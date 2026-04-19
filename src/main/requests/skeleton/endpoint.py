from dataclasses import dataclass
from enum import Enum

from src.main.models.base_model import BaseModel
from src.main.models.create_account_response import CreateAccountResponse
from src.main.models.create_user_request import CreateUserRequest
from src.main.models.create_user_response import CreateUserResponse
from src.main.models.deposit_request import DepositRequest
from src.main.models.deposit_response import DepositResponse
from src.main.models.login_user_request import LoginUserRequest
from src.main.models.login_user_response import LoginUserResponses
from src.main.models.transfer_request import TransferRequest
from src.main.models.transfer_response import TransferResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: BaseModel
    response_model: BaseModel


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(
        url='/admin/users',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_GET_ALL_USER = EndpointConfig(
        url='/admin/users',
        request_model=None,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfig(
        url='/admin/users',
        request_model=None,
        response_model=None
    )

    LOGIN_USER = EndpointConfig(
        url='/auth/login',
        request_model=LoginUserRequest,
        response_model=LoginUserResponses
    )

    CREATE_ACCOUNT = EndpointConfig(
        url='/accounts',
        request_model=None,
        response_model=CreateAccountResponse
    )

    GET_ACCOUNT = EndpointConfig(
        url='/accounts',
        request_model=None,
        response_model=CreateAccountResponse
    )

    DEPOSIT_ACCOUNT = EndpointConfig(
        url='/accounts/deposit',
        request_model=DepositRequest,
        response_model=DepositResponse
    )

    TRANSFER_MONEY = EndpointConfig(
        url='/accounts/transfer',
        request_model=TransferRequest,
        response_model=TransferResponse
    )

    GET_CUSTOMER_ACCOUNTS = EndpointConfig(
        url='/customer/accounts',
        request_model=None,
        response_model=CreateAccountResponse
    )



