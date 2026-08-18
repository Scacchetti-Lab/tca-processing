'''
--- Chats ---
POST   /chats                            # Inicia uma nova sessão com a mensagem do usuário 
POST   /chats/{id}/messages              # envia mensagem na mesma sessão
POST   /chats/meetings/{id}/feedback     # Gera um feedback de uma reunião especicada pelo seu ID
POST   /chats/user/{id}/feedback         # Gera um feedback para um usuário especicada pelo seu ID
POST   /chats/meetings/{id}/predict      # Gera uma previsão com base na transcrição da última reunião 
'''

import traceback

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.response_model import ResponseBaseModel as _ResponseBaseModel, ResponseModel as _ResponseModel
import app.services.chats_service as _ch

_router = APIRouter()

@_router.post('/', response_model=_ResponseBaseModel, status_code=status.HTTP_200_OK)
async def init_chat(message: str):
    try:
        response = await _ch.init_ai_session(message)

        if not response.is_valid:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Falha durante o processo de iniciar um chat')

        return JSONResponse(
            status_code=response.status,
            content=response.content,
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
            content=_ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
            media_type="application/json"
        )

@_router.post('/{history_id}/messages')
async def send_message_to_chat(message: str, history_id: str):
    try:
        response = await _ch.make_ai_response(message, history_id)

        if not response.is_valid:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Ocorreu um erro durante a tentativa de continuar o chat')
        
        return JSONResponse(
            status_code=response.status,
            content=response.content,
            media_type="application/json",
        )
    except HTTPException as httpex:
        return JSONResponse(
            status_code=httpex.status_code,
            content=_ResponseModel(status=httpex.status_code, message=httpex.detail, is_valid=False).__dict__,
            media_type='application/json'
        )
    except Exception as ex:
        print(f'\033[1;31m[ERRO] {ex}\033[m')
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
            media_type="application/json"
        )