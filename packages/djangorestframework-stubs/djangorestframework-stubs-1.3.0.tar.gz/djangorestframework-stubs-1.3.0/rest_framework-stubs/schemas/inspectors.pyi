from typing import Any, Mapping, Pattern

class ViewInspector:
    header_regex: Pattern = ...
    instance_schemas: Mapping[str, Any] = ...
    def __init__(self) -> None: ...
    def __get__(self, instance: Any, owner: Any): ...
    def __set__(self, instance: Any, other: Any) -> None: ...
    @property
    def view(self): ...
    @view.setter
    def view(self, value: Any) -> None: ...
    def get_description(self, path: Any, method: Any) -> str: ...

class DefaultSchema(ViewInspector): ...
