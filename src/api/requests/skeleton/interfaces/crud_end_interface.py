from typing import Optional, Protocol
from src.api.models.base_model import BaseModel
import requests
from src.api.requests.skeleton.endpoint import Endpoint

class CrudEndpointInterface(Protocol):
    def post(self, model: BaseModel) -> requests.Response: ...

    def get(self, endpoint: Optional["Endpoint"] = None, locator: Optional[str] = None,
            params: Optional[dict] = None) -> requests.Response: ...

    def delete(self, locator: str) -> requests.Response: ...
