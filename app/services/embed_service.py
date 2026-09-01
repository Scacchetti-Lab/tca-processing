from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from app.models import meeting, client
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

def _format_meeting_to_embbeding(raw_meeting: meeting):
    partes = [
        f"Reunião: {raw_meeting.title}",
        f"Cliente: {raw_meeting.client.name}",
        f"Tipo: {raw_meeting.type}",
    ]
    if raw_meeting.priority:
        partes.append(f"Prioridade: {raw_meeting.priority}")
    if raw_meeting.summary:
        partes.append(f"Resumo: {raw_meeting.summary}")
    if raw_meeting.feedback:
        partes.append(f"Feedback: {raw_meeting.feedback}")
    return ". ".join(partes)


def _format_client_to_embbeding(raw_client: client):
    resumos = " ".join(m.summary for m in raw_client.meetings if m.summary)
    return (
        f"{raw_client.name}, também conhecida como {raw_client.fantasy_name}. "
        f"Faturamento mensal de R$ {raw_client.revenue}. "
        f"Status atual do relacionamento: {raw_client.status}. "
        f"Histórico de reuniões: {resumos}"
    )
    
def generate_embeds(raw_model, model: SentenceTransformer):
    if isinstance(raw_model, meeting):
        formatted = _format_meeting_to_embbeding(raw_model)
    elif isinstance(raw_model, client):
        formatted = _format_client_to_embbeding(raw_model)
    else:
        return model.encode(raw_model).tolist()

    return model.encode(formatted).tolist()

    