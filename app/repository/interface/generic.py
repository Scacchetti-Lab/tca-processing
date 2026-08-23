from abc import ABC, abstractmethod
from uuid import UUID

from sqlmodel import SQLModel
from app.types.response_model import RespositoryModel

class GenericInterface(ABC):
    @abstractmethod
    def get_model_by_id(self, model: type[SQLModel], model_id: UUID) -> RespositoryModel:
        pass

    @abstractmethod
    def add_model(self, data: SQLModel) -> None:
        pass