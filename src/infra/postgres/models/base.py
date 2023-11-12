import abc
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class BaseModel(metaclass=abc.ABCMeta):
    table_name: str
