from os import getenv as __getenv
from dotenv import load_dotenv as __load_dotenv
from google import genai as __genai
from google.genai.interactions import Interaction
from app.constants.ai_context import FEEDBACK_TONES as _FEEDBACK_TONES, TRANSCRIPT_CONTEXT as _TRANSCRIPT_CONTEXT
from app.models.chats_models import InteractionCreateModel as __InteractionCreateModel
from app.models.transcripts_models import TranscriptAnalyse
from app.models.response_model import ResponseModel
from fastapi import status

__load_dotenv()

__GEMINI_API_KEY = __getenv("GEMINI_API_KEY")
__GEMINI_MODEL_NAME = __getenv("GEMINI_MODEL_NAME")

__client = __genai.Client(api_key=__GEMINI_API_KEY)

def analyse_transcript(transcript: str) -> ResponseModel:
    try:
        transcript_analysed = _create_simple_interactor(transcript, _TRANSCRIPT_CONTEXT)

        return ResponseModel(
                status=status.HTTP_200_OK,
                message=transcript_analysed.model_dump_json(),
                is_valid=True
            )
    except Exception as ex:
        print(ex)
        return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}"
            )

async def send_message(user_message: str, previous_interaction_id: str | None = None):
    pass

async def generate_feedback(transcript: str, tone: _FEEDBACK_TONES):
    pass

async def generate_prediction(last_transcript: str):
    pass

def _create_simple_interactor(request: str, context: str) -> TranscriptAnalyse:
    prompt = f'Analise a seguinte transcrição de reunião e retorne o JSON estruturado conforme instruído:\n\n{request}'
    
    interaction = __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=prompt,
        generation_config={"thinking_level": "medium", "temperature": 0.2},
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": TranscriptAnalyse.model_json_schema()
        },
        system_instruction=context,
        store=False,
        stream=False,
    )

    if not isinstance(interaction, Interaction):
        raise TypeError("Resposta inesperada da API: esperava Interaction, recebeu Stream.")

    if interaction.output_text is None:
        raise ValueError("A IA não retornou conteúdo de texto na análise da transcrição.")

    return TranscriptAnalyse.model_validate_json(interaction.output_text)

def _create_stream_interactor(model: __InteractionCreateModel):
    return __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=model.request,
        previous_interaction_id=model.interaction_id,
        generation_config={
            "thinking-level": "medium",
        },
        store=True
    )
