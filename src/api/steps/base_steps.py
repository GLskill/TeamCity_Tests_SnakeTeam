from typing import Any


class BaseSteps:
    def __init__(self, created_objects: list[Any] = None):
        self.created_objects = created_objects if created_objects is not None else []
