from typing_extensions import Self
from pydantic import BaseModel

class ResponseBaseModel(BaseModel):
    status: int
    message: str
    is_valid: bool


class ResponseModel:
    def __init__(self, status: int, message: str, is_valid: bool = False) -> None:
        self.status = status
        self.message = message
        self.is_valid = is_valid