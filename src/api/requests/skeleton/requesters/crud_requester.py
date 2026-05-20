from typing import TypeVar, Optional, Union

import requests

from src.api.configs.config import Config
from src.api.models.base_model import BaseModel
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.http_request import HttpRequest
from src.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface

T = TypeVar('T', bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpointInterface):

    @property
    def base_url(self) -> str:
        return f"{Config.get('baseurl')}"

    def post(self, model: Optional[T], endpoint: Endpoint = None, locator: str = None,
             suffix: str = None) -> requests.Response:
        ep = endpoint or self.endpoint
        url = f"{self.base_url}{ep.value.url}"
        if locator:
            url = f"{url}/{locator}"
        if suffix:
            url = f"{url}/{suffix}"
        response = requests.post(url=url, json=model.model_dump() if model is not None else None, headers=self.headers)
        self.response_spec(response)
        return response

    def get(self, endpoint: Endpoint = None, locator: str = None, params: dict = None,
            accept: str = None) -> requests.Response:
        ep = endpoint or self.endpoint
        url = f'{self.base_url}{ep.value.url}'
        if locator:
            url = f'{url}/{locator}'
        headers = {**self.headers, 'Accept': accept} if accept else self.headers
        response = requests.get(url=url, headers=headers, params=params)
        self.response_spec(response)
        return response

    def put(self, locator: str, body: Union[T, str], endpoint: Endpoint = None) -> requests.Response:
        ep = endpoint or self.endpoint
        url = f'{self.base_url}{ep.value.url}/{locator}'
        if isinstance(body, str):
            headers = {**self.headers, 'Content-Type': 'text/plain', 'Accept': 'text/plain'}
            response = requests.put(url=url, data=body, headers=headers)
        else:
            response = requests.put(url=url, json=body.model_dump(), headers=self.headers)
        self.response_spec(response)
        return response

    def delete(self, locator: str, endpoint: Endpoint = None) -> requests.Response:
        ep = endpoint or self.endpoint
        url = f'{self.base_url}{ep.value.url}/{locator}'
        response = requests.delete(url=url, headers=self.headers)
        self.response_spec(response)
        return response
