'''
--- Chats ---
POST   /chats                            # Inicia uma nova sessão com a mensagem do usuário 
POST   /chats/{id}/messages              # envia mensagem na mesma sessão
POST   /chats/user/{id}/feedback         # Gera um feedback para um usuário especicada pelo seu ID
POST   /chats/meetings/{id}/predict      # Gera uma previsão com base no id da reunião da última reunião 
POST   /chats/client/{id}/predict        # Gera uma previsão com base no id do client da última reunião 
'''

import traceback
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse
from app.types.chats_models import *
from app.types.response_model import ResponseBaseModel as _ResponseBaseModel, ResponseModel as _ResponseModel
import app.services.chats_service as _ch
import app.services.predit_service as _pd
from typing import Annotated
from app.db_connect import SessionDep
from app.deps import ModelDep

_router = APIRouter()

@_router.post('/messages', response_model=_ResponseBaseModel, status_code=status.HTTP_200_OK)
async def init_chat(payload: Annotated[ChatMessagesResponse, Body()], session: SessionDep, model: ModelDep):
    try:
        response = await _ch.make_ai_response(payload.message, session, model, payload.previous_interact_id)

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