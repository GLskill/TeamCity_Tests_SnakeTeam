from dataclasses import dataclass


@dataclass
class GeneratingRule:
    regex: str = None
    skip: bool = False

