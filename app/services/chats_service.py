from uuid import UUID
from app.db_connect import SessionDep
from app.helpers.is_valid_json import is_valid_json
from app.repository.transcript import TranscriptRepository
from app.types.response_model import ResponseModel
from app.services.gemini_client_service import send_message
from app.services.embed_service import generate_embeds
from fastapi import status
from app.deps import ModelDep
from json import dumps

async def make_ai_response(message: str, session: SessionDep, model: ModelDep, previous_id: str | None = None):
    try:
        transcript_contexts = search_transcripts_relationated(message, session, model)

        if not is_valid_json(transcript_contexts):
             message = __make_rag_input(message, transcript_contexts)

        response = await send_message(message, previous_id)
        return response
    except Exception as ex:
        print(ex)
        return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}"
            )

def search_transcripts_relationated(prompt: str, session: SessionDep, model: ModelDep) -> str:
    transcript_repository = TranscriptRepository(session)
    embedd_prompt = generate_embeds(prompt, model)

    result = transcript_repository.search_simmiliarities(embedd_prompt)

    if not result.is_valid:
        return dumps({'status': result.is_valid, 'message': result.message})
    chunks_founded = result.result
    return __make_rag_context(chunks_founded)


def __make_rag_context(chunks) -> str:
    return "\n\n".join(
        f"[Trecho da reunião {c.tc_transcript_id}]\n{c.tc_chunk_text}"
        for c in chunks
    )

def __make_rag_input(prompt, context) -> str:
    return f"""Contexto recuperado de reuniões anteriores:
    {context}

    Pergunta do usuário: {prompt}"""