from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from app.models import meeting, client
from app.models.transcript import transcript_chunk
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from app.db_connect import SessionDep
from app.repository.transcript import TranscriptRepository
from app.types.response_model import ResponseModel
from fastapi import status

_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def add_transcript_embeddings(transcript_id: str, chunks: list[str], embeddings, session: SessionDep) -> ResponseModel:
    try:
        transcript_uuid = UUID(transcript_id)
        transcript_repository = TranscriptRepository(session)
    
        chunk_models: list['transcript_chunk'] = []
        for chunk, embedding in zip(chunks, embeddings):
            chunk_models.append(transcript_chunk(
                tc_id=uuid4(),
                tc_chunk_text=chunk,
                tc_created_at=datetime.now(),
                tc_embeddings=embedding,
                tc_transcript_id=transcript_uuid
            ))
        res = transcript_repository.save_chunks(chunk_models)

        if not res.is_valid:
            raise RuntimeError(res.message)

        session.commit()
        session.refresh(chunk_models)    

        return ResponseModel(
            status=status.HTTP_201_CREATED,
            message=res.message,
            is_valid=True,
            content=res.result
        )
    except Exception as ex:
        raise ex

def generate_chunks(transcript_sliced: str):

    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '. ', ' ', ''],
        chunk_size=800,
        chunk_overlap=160,
        length_function=len
    )
    return text_splitter.split_text(transcript_sliced)

def _format_meeting_to_embbeding(raw_meeting: meeting):
    partes = [
        f"Reunião: {raw_meeting.mt_title}",
        f"Cliente: {raw_meeting.mt_client.cl_name}",
        f"Tipo: {raw_meeting.mt_type}",
    ]
    if raw_meeting.mt_priority:
        partes.append(f"Prioridade: {raw_meeting.mt_priority}")
    if raw_meeting.mt_summary:
        partes.append(f"Resumo: {raw_meeting.mt_summary}")
    if raw_meeting.mt_feedback:
        partes.append(f"Feedback: {raw_meeting.mt_feedback}")
    return ". ".join(partes)


def _format_client_to_embbeding(raw_client: client):
    resumos = " ".join(m.mt_summary for m in raw_client.cl_meetings if m.mt_summary)
    return (
        f"{raw_client.cl_name}, também conhecida como {raw_client.cl_fantasy_name}. "
        f"Faturamento mensal de R$ {raw_client.cl_revenue}. "
        f"Status atual do relacionamento: {raw_client.cl_status}. "
        f"Histórico de reuniões: {resumos}"
    )
    
def generate_embeds(raw_model):
    if isinstance(raw_model, List):
        return _model.encode(raw_model).tolist()
    elif isinstance(raw_model, meeting):
        formatted = _format_meeting_to_embbeding(raw_model)
    elif isinstance(raw_model, client):
        formatted = _format_client_to_embbeding(raw_model)
    else:
        return None

    return _model.encode(formatted).tolist()

    