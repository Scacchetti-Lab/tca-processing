'''
--- Transcrições ---
POST   /transcripts/process         # extração via Gemini (faz a limpeza e extração de infos com AI)

-- JAVA --
POST   /transcripts                      # upload da transcrição (JSON/CSV)
GET    /transcripts/{id}                 # detalhe + resultado da extração
GET    /transcripts                      # lista (filtros: ?userId=, ?dateFrom=, etc.)
GET    /transcripts/{id}/scores          # scores (performance + estratégico juntos)
'''

from fastapi import APIRouter
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

router = APIRouter();

@router.post("/process")
async def process_transcript():
    pass