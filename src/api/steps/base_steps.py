from typing import Any


class BaseSteps:
    def __init__(self, created_objects: list[Any] = None, headers: dict = None):
        from src.api.specs.request_spec import RequestSpecs
        self.created_objects = created_objects if created_objects is not None else []
        self.headers = headers if headers is not None else RequestSpecs.admin_base_headers()
