from typing import Dict, Callable, Optional
from src.api.requests.skeleton.endpoint import Endpoint


class HttpRequest:
    def __init__(self, request_spec: Dict[str, str], response_spec: Callable, endpoint: Optional[Endpoint] = None):
        self.headers = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec

