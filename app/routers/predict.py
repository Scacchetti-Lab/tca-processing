from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
import app.services.predit_service as _pd
from app.types.response_model import ResponseModel as _ResponseModel
from app.types.chats_models import ClientPredictRequest, MeetingPredictRequest
from traceback import format_exc
from app.db_connect import SessionDep as __SessionDep

_router = APIRouter()


@_router.post('/meeting')
async def predict_next_meeting(payload: Annotated[MeetingPredictRequest, Body()], session: __SessionDep):
    try:
        predict_data = await _pd.predict_meeting(payload.meeting_id, session)

        print('to aqui 7')
        if predict_data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Falha ao gerar previsão de reunião", media_type="application/json")

        print('cabo')
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=_ResponseModel(status.HTTP_201_CREATED, content={"predict": predict_data}, message="Previsão criada.").__dict__,
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
        print(format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
            media_type="application/json"
        )

@_router.post('/client')
async def predict_client_status(payload: Annotated[MeetingPredictRequest, Body()], session: __SessionDep):
    pass
#     try:
        

            
            
#         return JSONResponse(
#             status_code=status.HTTP_201_CREATED,
#             content=predict,
#             media_type="application/json",
#         )
#     except HTTPException as httpex:
#         return JSONResponse(
#             status_code=httpex.status_code,
#             content=_ResponseModel(status=httpex.status_code, message=httpex.detail, is_valid=False).__dict__,
#             media_type='application/json'
#         )
#     except Exception as ex:
#         print(f'\033[1;31m[ERRO] {ex}\033[m')
#         print(traceback.format_exc())
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content=_ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
#             media_type="application/json"
#         )