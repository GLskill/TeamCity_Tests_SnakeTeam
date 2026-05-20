from typing import TypeVar, Optional, Union

from pydantic import TypeAdapter

from src.api.models.base_model import BaseModel
from src.api.requests.skeleton.endpoint import Endpoint
from src.api.requests.skeleton.http_request import HttpRequest
from src.api.requests.skeleton.requesters.crud_requester import CrudRequester

T = TypeVar('T', bound=BaseModel)


class ValidatedCrudRequester(HttpRequest):
    def __init__(self, request_spec, endpoint: Endpoint, response_spec):
        super().__init__(request_spec, response_spec, endpoint)
        self.crud_requester = CrudRequester(request_spec=request_spec, endpoint=endpoint, response_spec=response_spec)
        self._adapter = TypeAdapter(self.endpoint.value.response_model)

    def post(self, model: Optional[T] = None, locator: Optional[str] = None):
        response = self.crud_requester.post(model=model, locator=locator)
        if not response.content:
            return None
        return self._adapter.validate_python(response.json())

    def get(self, locator: Optional[str] = None, params: Optional[dict] = None):
        response = self.crud_requester.get(locator=locator, params=params)
        return self._adapter.validate_python(response.json())

    def put(self, locator: str, body: Union[T, str]) -> None:
        self.crud_requester.put(locator=locator, body=body)

    def delete(self, locator: str) -> None:
        self.crud_requester.delete(locator=locator)
