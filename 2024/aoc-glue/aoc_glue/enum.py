import enum
import platform

if platform.python_implementation() == "PyPy":
    from strenum import StrEnum as StrEnum
else:
    from enum import StrEnum as StrEnum


class AnnotatedEnum(enum.Enum):
    def __new__(cls, *args, **kwargs):
        for annotation in cls.__annotations__:
            setattr(cls, annotation, enum.auto())
        return super().__new__(cls, *args, **kwargs)
