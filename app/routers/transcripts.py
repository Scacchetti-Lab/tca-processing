'''
--- Transcrições ---
POST   /transcripts/process         # extração via Gemini (faz a limpeza e extração de infos com AI)
'''

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.services import gemini_client_service as gen, transcripts_service as trs
from app.models.transcripts_models import TranscriptAnalyse
     
router = APIRouter();

@router.post("/process", status_code=status.HTTP_201_CREATED)
async def process_transcript(transcript: str) -> JSONResponse:
    try:
        cleaned_text = trs.clean_transcript(transcript)
        gen_analysed = await gen.analyse_transcript(cleaned_text)

        if (TranscriptAnalyse.model_validate(gen_analysed) == None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUES, detail='Falha no retorno do processamento da transcrição')

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=gen_analysed,
            media_type="application/json"
        )
    except Exception as ex:
        print(f'\033[1;31m[ERRO] {ex}\033[m')
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Ocorreu um erro inesperado durante o processamento" },
            media_type="application/json"
        )