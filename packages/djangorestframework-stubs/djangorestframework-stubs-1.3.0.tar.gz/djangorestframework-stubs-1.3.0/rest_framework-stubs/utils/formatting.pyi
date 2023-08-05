from typing import Any, Union

def remove_trailing_string(content: str, trailing: str) -> str: ...
def dedent(content: Union[str, bytes]) -> str: ...
def camelcase_to_spaces(content: str) -> str: ...
def markup_description(description: str) -> str: ...

class lazy_format:
    format_string: str = ...
    result: str = ...
    args: Any
    kwargs: Any
    def __init__(self, format_string: str, *args: Any, **kwargs: Any): ...
    def __str__(self) -> str: ...
