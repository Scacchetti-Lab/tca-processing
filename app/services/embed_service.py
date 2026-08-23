from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from app.models import meeting, client

_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def generate_chunks(transcript_sliced: str):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '. ', ' ', ''],
        chunk_size=800,
        chunk_overlap=160,
        length_function=len
    )
    return text_splitter.split_text(transcript_sliced)

def generate_transcript_embeds(transcript_chunks: list[str]):
    return _model.encode(transcript_chunks)

def generate_embeds(raw_model):
    if isinstance(raw_model, meeting):
        return _generate_meeting_embeds(raw_model)
    elif isinstance(raw_model, client):
        return _generate_client_embeds(raw_model)
    else:
        return None


def _generate_meeting_embeds(raw_meeting: meeting):
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
    text_to_embed = ". ".join(partes)

    return _model.encode(text_to_embed)


def _generate_client_embeds(raw_client: client):
    resumos = " ".join(m.mt_summary for m in raw_client.cl_meetings if m.mt_summary)
    text_to_embed = (
        f"{raw_client.cl_name}, também conhecida como {raw_client.cl_fantasy_name}. "
        f"Faturamento mensal de R$ {raw_client.cl_revenue}. "
        f"Status atual do relacionamento: {raw_client.cl_status}. "
        f"Histórico de reuniões: {resumos}"
    )
    return _model.encode(text_to_embed)
