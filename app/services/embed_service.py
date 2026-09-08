from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from app.models import meetings, clients
from app.models.transcript import transcript_chunks
from uuid import UUID, uuid4
from datetime import datetime
from app.db_connect import SessionDep
from app.repository.transcript import TranscriptRepository
from app.types.response_model import ResponseModel
from fastapi import status

def add_transcript_embeddings(transcript_id: str, chunks: list[str], embeddings, session: SessionDep) -> ResponseModel:
    try:
        transcript_uuid = UUID(transcript_id)
        transcript_repository = TranscriptRepository(session)
    
        chunk_models: list['transcript_chunks'] = []
        for chunk, embedding in zip(chunks, embeddings):
            chunk_models.append(transcript_chunks(
                id=uuid4(),
                chunk_text=chunk,
                created_at=datetime.now(),
                embedding=embedding,
                transcript_id=transcript_uuid
            ))
        res = transcript_repository.save_chunks(chunk_models)

        if not res.is_valid:
            raise RuntimeError(res.message)

        session.commit()

        return ResponseModel(
            status=status.HTTP_201_CREATED,
            message=res.message,
            is_valid=True,
            content={"result": res.message}
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

def _format_meeting_to_embbeding(raw_meeting: meetings):
    partes = [
        f"Reunião: {raw_meeting.title if raw_meeting.title else "Título não definido"}",
        f"Cliente: {raw_meeting.client.name}",
        f"Sumário: {raw_meeting.summary if raw_meeting.summary else "Sumário não definido"}",
        f"Representante do Cliente: {raw_meeting.client_represent}",
        f"Média de Performance: {"Não Definida" if not raw_meeting.performance_avg or raw_meeting.performance_avg <= 0 else raw_meeting.performance_avg}",
        f"Prioridade: {raw_meeting.priority}",
    ]
    return ". ".join(partes)


def _format_client_to_embbeding(raw_client: clients):
    resumos = " ".join(m.summary for m in raw_client.meetings if m.summary)
    return (
        f"{raw_client.name}, também conhecida como {raw_client.fantasy_name}. "
        f"Faturamento mensal de R$ {raw_client.revenue}. "
        f"Status atual do relacionamento: {raw_client.status}. "
        f"Histórico de reuniões: {resumos}"
        f"Contato do cliente: {raw_client.email if raw_client.email else raw_client.phone if raw_client else "Não definido"}"
    )
    
def generate_embeds(raw_model, model: SentenceTransformer):
    if isinstance(raw_model, meetings):
        formatted = _format_meeting_to_embbeding(raw_model)
    elif isinstance(raw_model, clients):
        formatted = _format_client_to_embbeding(raw_model)
    else:
        return model.encode(raw_model).tolist()

    return model.encode(formatted).tolist()

    