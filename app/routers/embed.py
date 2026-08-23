'''
POST    /embed/chunk           # Gera chunks da transcrição e cria embeddings referente a elas
POST    /embed/client          # Cria embeddings com base no histórico do cliente salvo
POST    /embed/meeting         # Cria embeddings com base no histórico da reunião salva
'''

from fastapi import APIRouter

_router = APIRouter()

@_router.post("/chunk")
def embed_transcript(transcript_id: str):
    pass

@_router.post("/client")
def embed_client(client_id: str):
    pass

@_router.post("/meeting")
def embed_meeting(meeting_id: str):
    pass