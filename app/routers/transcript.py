'''
--- Transcrições ---
POST   /transcripts                      # upload da transcrição (JSON/CSV)
POST   /transcripts/{id}/clean           # limpeza (pandas) -> ou automático dentro do upload
POST   /transcripts/{id}/process         # extração via Gemini
GET    /transcripts/{id}                 # detalhe + resultado da extração
GET    /transcripts                      # lista (filtros: ?userId=, ?dateFrom=, etc.)
GET    /transcripts/{id}/scores          # scores (performance + estratégico juntos)
'''

from fastapi import APIRouter

router = APIRouter("transcript");

