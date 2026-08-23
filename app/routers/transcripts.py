'''
--- Transcrições ---
POST   /transcripts/process         # extração via Gemini (faz a limpeza e extração de infos com AI)
'''

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.services import gemini_client_service as gen, transcripts_service as trs
from app.types.transcripts_models import TranscriptAnalyse, TranscriptReturnJson, TranscriptPayload
from app.types.response_model import ResponseModel, ResponseBaseModel
from app.constants.transcript import SCORE_TYPE
import traceback
from pydantic import ValidationError
     
router = APIRouter()

@router.post("/process", response_model=ResponseBaseModel, status_code=status.HTTP_201_CREATED)
async def process_transcript(transcript_id: str, score_type: SCORE_TYPE) -> JSONResponse:
    try:
        if (score_type not in ['STRATEGIC', 'PERFORMANCE']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='O tipo do score enviado é inválido.')

        transcript_data = trs.get_transcript_by_id(transcript_id)

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
            score_type=score_type,
            transcript=cleaned_text
        )
        
        gen_analysed = gen.analyse_transcript(payload)
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
    except Exception as ex:
        print(f'\033[1;31m[ERRO] {ex}\033[m')
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseModel(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Ocorreu um erro inesperado durante o processamento").__dict__,
            media_type="application/json"
        )