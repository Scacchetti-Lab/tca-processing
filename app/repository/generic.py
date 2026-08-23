from uuid import UUID
from sqlmodel import SQLModel
from app.repository.interface.generic import GenericInterface
from app.db_connect import SessionDep
from app.types.response_model import RespositoryModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.client import client
    from app.models.meeting import meeting

class GenericRepository(GenericInterface):
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_model_by_id(self, model: type[SQLModel], model_id: UUID) -> RespositoryModel:
        try:
            data_value = self.session.get(model, model_id)

            if not data_value:
                return RespositoryModel(message='Nenhum cliente encontrada com esse ID')

            return RespositoryModel(
                is_valid=True,
                message='Cliente encontrada!',
                result=data_value
            )
        except Exception as ex:
            print(ex)
            return RespositoryModel(
                is_valid=True,
                message='Cliente encontrada!',
                result=None
            )

    def add_model(self, data: SQLModel) -> None:
        self.session.add(data)