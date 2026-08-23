'''
POST    /embed/chunk           # Gera chunks da transcrição e cria embeddings referente a elas
POST    /embed/client          # Cria embeddings com base no histórico do cliente salvo
POST    /embed/meeting         # Cria embeddings com base no histórico da reunião salva
'''

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from traceback import format_exc
from app.types.response_model import ResponseModel
from app.services.transcripts_service import get_transcript_by_id
from app.services.embed_service import generate_chunks, generate_embeds, add_transcript_embeddings
from app.db_connect import SessionDep

_router = APIRouter()

@_router.post("/chunk")
def embed_transcript(transcript_id: str, session: SessionDep) -> JSONResponse:
    try:
        raw_transcript = get_transcript_by_id(transcript_id)

        if not raw_transcript:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Nenhuma transcrição foi encontrada com esse ID'
            )
        chunks = generate_chunks(raw_transcript)
        embeddings = generate_embeds(chunks)

        if not embeddings:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Falha ao gerar embeddings'
            )

        result = add_transcript_embeddings(transcript_id, chunks, embeddings, session)

        if not result.is_valid:
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail='Não foi possível adicionar os dados da trancrição',
            )

        return JSONResponse(
            status_code=result.status,
            content=result.__dict__,
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


@_router.post("/client")
def embed_client(client_id: str) -> JSONResponse:
    pass

@_router.post("/meeting")
def embed_meeting(meeting_id: str) -> JSONResponse:
    pass