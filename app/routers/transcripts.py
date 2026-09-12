'''
--- Transcrições ---
POST   /transcripts/process         # extração via Gemini (faz a limpeza e extração de infos com AI)
'''

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from app.services import gemini_client_service as gen, transcripts_service as trs
from app.types.transcripts_models import TranscriptAnalyse, TranscriptReturnJson, TranscriptPayload, TranscriptRequest
from app.types.response_model import ResponseModel, ResponseBaseModel
import traceback
from pydantic import ValidationError
from app.db_connect import SessionDep
from typing import Annotated
     
router = APIRouter()

@router.post("/process", response_model=ResponseBaseModel, status_code=status.HTTP_201_CREATED)
async def process_transcript(request: Annotated[TranscriptRequest, Body()], session: SessionDep) -> JSONResponse:
    try:
        if (request.profile not in ['SALESPERSON', 'DIRECTOR', 'MANAGER']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='O perfil enviado é inválido.')

        transcript_data = trs.get_transcript_by_id(request.transcript_id, session)

        if transcript_data is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='O ID fornecido é incorreto.'
            )

        cleaned_text = ''
        if isinstance(transcript_data, str):
            cleaned_text = trs.clean_transcript(transcript_data)
        elif isinstance(transcript_data, TranscriptReturnJson):
            transcript_data = TranscriptReturnJson.model_validate(transcript_data)
            cleaned_text = trs.clean_transcript(transcript_data.transcription)

        payload = TranscriptPayload(
            profile=request.profile,
            transcript=cleaned_text,
            client=request.client_context
        )
        
        gen_analysed = await gen.analyse_transcript(payload)
        TranscriptAnalyse.model_validate(gen_analysed.content) 

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=gen_analysed.__dict__,
            media_type="application/json"
        )

    except ValidationError as vex:
        print(vex)
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Erro ao obter transcrição analisada pela IA").__dict__
        )
    except HTTPException as httpex:
        print(httpex)
        print(traceback.format_exc())
        return JSONResponse(
            status_code=httpex.status_code,
            content=ResponseModel(status=httpex.status_code, message=httpex.detail, is_valid=False).__dict__
        )
    except ValueError as vex:
        print(f'\033[1;31m[ERRO] {vex}\033[m')
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ResponseModel(status=status.HTTP_400_BAD_REQUEST, message=f"{vex}").__dict__,
            media_type="application/json"
        )
    except Exception as ex:
        print(f'\033[1;31m[ERRO] {ex}\033[m')
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
            media_type="application/json"
        )