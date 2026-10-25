import traceback
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse
from app.types.chats_models import *
from app.types.response_model import ResponseBaseModel as _ResponseBaseModel, ResponseModel as _ResponseModel
import app.services.chats_service as _ch
from typing import Annotated
from app.db_connect import SessionDep
from app.deps import ModelDep

router = APIRouter()

@router.post('/messages', response_model=_ResponseBaseModel, status_code=status.HTTP_200_OK)
async def init_chat(payload: Annotated[ChatMessagesResponse, Body()], session: SessionDep, model: ModelDep):
    try:
        response = await _ch.make_ai_response(payload, session, model)

        if not response.is_valid:
            raise HTTPException(response.status, response.message or 'Falha durante o processo de conversar com o chat')

        return JSONResponse(
            status_code=response.status,
            content=response.__dict__,
            media_type="application/json",
        )
    except HTTPException as httpex:
        return JSONResponse(
            status_code=httpex.status_code,
            content=_ResponseModel(status=httpex.status_code, message=httpex.detail, is_valid=False).__dict__,
            media_type="application/json"
        )
    except Exception as ex:
        print(f'\033[1;31m[ERRO] {ex}\033[m')
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento", is_valid=False).__dict__,
            media_type="application/json"
        )