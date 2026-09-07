from uuid import UUID
from sqlmodel import SQLModel
from app.repository.interface.generic import GenericInterface
from app.db_connect import SessionDep
from app.types.response_model import RespositoryModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.client import clients
    from app.models.meeting import meetings

class GenericRepository(GenericInterface):
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_model_by_id(self, model: type[SQLModel], model_id: UUID) -> RespositoryModel:
        try:
            data_value = self.session.get(model, model_id)

            if not data_value:
                return RespositoryModel(message='Nenhum cliente encontrado com esse ID')

            return RespositoryModel(
                is_valid=True,
                message='Cliente encontrado!',
                result=data_value
            )
        except Exception as ex:
            print(ex)
            return RespositoryModel(
                is_valid=True,
                message='Cliente não foi encontrado!',
                result=None
            )

    def add_model(self, data: SQLModel) -> None:
        self.session.add(data)