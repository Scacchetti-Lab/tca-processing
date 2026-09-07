from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from traceback import format_exc
from app.types.response_model import ResponseModel, ResponseBaseModel
from app.services.transcripts_service import get_transcript_by_id
from app.services.embed_service import generate_chunks, generate_embeds, add_transcript_embeddings
from app.db_connect import SessionDep
from app.deps import ModelDep
from app.services.generic_service import get_sqlmodel_by_id, add_sqlmodel_embeddings
from app.models.client import client as cl_model
from app.models.meeting import meeting as mt_model
from typing import Literal, Annotated
from app.types.embed_models import *

_router = APIRouter()

@_router.post("/chunk", response_model=ResponseBaseModel, status_code=status.HTTP_201_CREATED)
def embed_transcript(payload: Annotated[ChunkRequets, Body()], session: SessionDep, ai_model: ModelDep) -> JSONResponse:
    '''Gera chunks da transcrição e cria embeddings referente a elas'''
    try:
        raw_transcript = get_transcript_by_id(payload.transcript_id, session)

        if not raw_transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Nenhuma transcrição foi encontrada com esse ID'
            )
        chunks = generate_chunks(raw_transcript)
        embeddings = generate_embeds(chunks, ai_model)

        if not embeddings:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Falha ao gerar embeddings'
            )

        result = add_transcript_embeddings(payload.transcript_id, chunks, embeddings, session)

        if not result.is_valid:
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail='Não foi possível adicionar os dados da trancrição',
            )

        return JSONResponse(
            status_code=result.status,
            content=ResponseModel(status=result.status, message='Chunks foram adicionados!', content={"result": result.message}).__dict__,
            media_type="application/json"
        )
    except HTTPException as httpex:
        session.rollback()
        print(httpex)
        print(format_exc())
        return JSONResponse(
            status_code=httpex.status_code,
            content=ResponseModel(status=httpex.status_code, message=httpex.detail, is_valid=False).__dict__,
            media_type="application/json"
        )
    except Exception as ex:
        session.rollback()
        print(f'\033[1;31m[ERRO] {ex}\033[m')
        print(format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
            media_type="application/json"
        )


@_router.post("/client", response_model=ResponseBaseModel, status_code=status.HTTP_200_OK)
def embed_client(payload: Annotated[ClientEmbedd, Body()], session: SessionDep, ai_model: ModelDep) -> JSONResponse:
    '''Cria embeddings com base no histórico do cliente salvo'''
    return __embed_meeting_or_client('client', payload.client_id, session, ai_model)

@_router.post("/meeting", response_model=ResponseBaseModel, status_code=status.HTTP_200_OK)
def embed_meeting(payload: Annotated[MeetingEmbedd, Body()], session: SessionDep, ai_model: ModelDep) -> JSONResponse:
    '''Cria embeddings com base no histórico da reunião salva'''
    return __embed_meeting_or_client('meeting', payload.meeting_id, session, ai_model)


def __embed_meeting_or_client(model_name: Literal['client', 'meeting'], model_id, session: SessionDep, ai_model: ModelDep) -> JSONResponse:
    try:
        base_model = cl_model if model_name == 'client' else mt_model

        model = get_sqlmodel_by_id(base_model, model_id, session)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Cliente não foi encontrado'
            )
        
        embeddings_generated = generate_embeds(model, ai_model)
        if not embeddings_generated:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Falha ao gerar embeddings'
            )

        match(model_name):
            case 'client':
                model.embeddings = embeddings_generated
            case 'meeting':
                model.embeddings = embeddings_generated
            case _:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Modelo fornecido não pode atribuir embeddings'
                )
            
        result = add_sqlmodel_embeddings(model, session)

        if not result.is_valid:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result.message,
            media_type="application/json"
        )
    except HTTPException as httpex:
        session.rollback()
        print(httpex)
        print(format_exc())
        return JSONResponse(
            status_code=httpex.status_code,
            content=ResponseModel(status=httpex.status_code, message=httpex.detail, is_valid=False).__dict__,
            media_type="application/json"
        )
    except Exception as ex:
        session.rollback()
        print(f'\033[1;31m[ERRO] {ex}\033[m')
        print(format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
            media_type="application/json"
        )