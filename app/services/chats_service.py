import asyncio
import traceback
from app.db_connect import SessionDep
from app.helpers.is_valid_json import is_valid_json
from app.repository.transcript import TranscriptRepository
from app.types.chats_models import ChatMessagesResponse
from app.types.response_model import ResponseModel
from app.services.gemini_client_service import send_message
from app.services.embed_service import generate_embeds
from fastapi import status
from app.deps import ModelDep
from json import dumps
from app.constants import ai_context as ai

async def make_ai_response(request: ChatMessagesResponse, session: SessionDep, model: ModelDep) -> ResponseModel:
    try:
        transcript_contexts = await asyncio.to_thread(
            search_transcripts_relationated, request.message, session, model
        )
        base_context = ai.CHATBOT_VOICE_CONTEXT if request.chat_model == "VOICE" else ai.CHATBOT_TEXT_CONTEXT

        if not is_valid_json(transcript_contexts):
            request.message = __make_rag_input(request.message, transcript_contexts)

        return await send_message(request.message, base_context, request.previous_interact_id)

    except Exception as ex:
        print(traceback.format_exc())
        return ResponseModel(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}",
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
        f"[Trecho da reunião] \n{c.chunk_text}"
        for c in chunks
    )

def __make_rag_input(prompt, context) -> str:
    return f"""Contexto recuperado de reuniões anteriores:
    {context}

    Pergunta do usuário: {prompt}"""