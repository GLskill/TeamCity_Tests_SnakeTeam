import inspect
from datetime import datetime, timedelta
import uuid
import rstr
import random
from typing import Any, Annotated, get_type_hints, get_origin, get_args
from src.api.generators.random_data import RandomData
from src.api.generators.generating_rule import GeneratingRule
from src.api.models.base_model import BaseModel


class RandomModelGenerator:
    _FIELD_GENERATORS = {
        'password': RandomData.get_password,
    }

    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}
        for field_name, annotated_type in type_hints.items():    # Сначала проверяем специальные генераторы
            if field_name in RandomModelGenerator._FIELD_GENERATORS:
                init_data[field_name] = RandomModelGenerator._FIELD_GENERATORS[field_name]()
                continue

            rule = None     # Остальная логика для полей с GeneratingRule
            actual_type = annotated_type
            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, GeneratingRule):
                        rule = ann
            if rule and rule.skip:
                default = inspect.signature(cls).parameters.get(field_name)
                init_data[field_name] = (
                    default.default
                    if default and default.default is not inspect.Parameter.empty
                    else None
                )
                continue
            if rule:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            else:
                value = RandomModelGenerator._generate_value(actual_type)
            init_data[field_name] = value
        return cls(**init_data)

    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is str and len(generated) <= 15 and '^' not in regex and '$' not in regex:
            unique_suffix = str(uuid.uuid4())[:8]
            generated = f"{generated}{unique_suffix}"
        if field_type is int:
            return int(generated)
        if field_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        try:
            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                return RandomModelGenerator.generate(field_type)
        except TypeError:
            pass
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(0, 1000)
        elif field_type is float:
            return round(random.uniform(0, 100.0), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is datetime:
            return datetime.now() - timedelta(seconds=random.randint(0, 100000))
        elif field_type is list:
            return [str(uuid.uuid4())[:5] for _ in random.randint(3, 10)]
        elif isinstance(field_type, type):
            return
