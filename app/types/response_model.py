from typing_extensions import Self
from pydantic import BaseModel

class ResponseBaseModel(BaseModel):
    status: int
    content: dict[str, str] | None
    message: str | None
    is_valid: bool


class ResponseModel:
    def __init__(self, status: int, content: dict[str, str] | None = None, message: str = '', is_valid: bool = False) -> None:
        self.status = status
        self.content = content
        self.message = message
        self.is_valid = is_valid