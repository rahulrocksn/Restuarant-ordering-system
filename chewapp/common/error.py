from typing import Optional, Tuple, TypeVar


class Error(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __str__(self):
        return f"Error {self.code}: {self.message}"


T = TypeVar("T")
Result = Tuple[Optional[T], Optional[Error]]
