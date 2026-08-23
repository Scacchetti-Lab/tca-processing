# ==================================================================================================================================
#  MÓDULO SERVICE CRIADO SOMENTE PARA QUE NÃO SEJA NECESSÁRIO CRIAR UM ARQUIVO COMPLETO PARA ALGUMAS OPERAÇÕES DE POUCAS ENTIDADES
# ==================================================================================================================================
from sqlmodel import SQLModel
from app.types.response_model import ResponseModel
from fastapi import status
from app.repository.generic import GenericRepository
from typing import TYPE_CHECKING
from uuid import UUID
from app.helpers.is_valid_uuid import is_valid_uuid
from traceback import format_exc

if TYPE_CHECKING:
    from app.db_connect import SessionDep

def get_sqlmodel_by_id(model: type[SQLModel], model_id: str, session: SessionDep) -> SQLModel | None:
    if not is_valid_uuid(model_id):
        raise TypeError('Id do modelo é inválido')

    return GenericRepository(session).get_model_by_id(model, UUID(model_id)).result


def add_sqlmodel_embeddings(new_model: SQLModel, session: SessionDep) -> ResponseModel:
    GenericRepository(session).add_model(new_model)
    session.commit()
    session.refresh(new_model)    
    return ResponseModel(
        status=status.HTTP_201_CREATED,
        message='Modelo adicionado!',
        is_valid=True,
    )