from typing_extensions import Any
from pydantic import BaseModel

class ResponseBaseModel(BaseModel):
    status: int
    content: dict[str, str] | None
    message: str | None
    is_valid: bool

class RespositoryBaseModel(BaseModel):
    is_valid: bool
    message: str
    result: Any

class ResponseModel:
    def __init__(self, status: int, content: dict[str, str] | None = None, message: str = '', is_valid: bool = False) -> None:
        self.status = status
        self.content = content
        self.message = message
        self.is_valid = is_valid

class RespositoryModel:
    def __init__(self, is_valid: bool = False, message: str = '', result: Any | None = None):
        self.is_valid = is_valid
        self.message = message
        self.result = result