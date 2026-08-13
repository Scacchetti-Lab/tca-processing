from os import getenv as __getenv
from dotenv import load_dotenv as __load_dotenv
from google import genai as __genai
from app.constants.ai_context import FEEDBACK_TONES as _FEEDBACK_TONES, TRANSCRIPT_CONTEXT as _TRANSCRIPT_CONTEXT
from app.models.chats_models import InteractionCreateModel as __InteractionCreateModel
from app.models.transcripts_models import TranscriptAnalyse
from app.models.response_model import ResponseModel
from fastapi import status, HTTPException

__load_dotenv()

__GEMINI_API_KEY = __getenv("GEMINI_API_KEY")
__GEMINI_MODEL_NAME = __getenv("GEMINI_MODEL_NAME")

__client = __genai.Client(api_key=__GEMINI_API_KEY)

async def analyse_transcript(transcript: str) -> TranscriptAnalyse | ResponseModel:
    try:
        response = _create_simple_interactor(transcript, _TRANSCRIPT_CONTEXT)

        if (response.output_text.length == 0):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="O Gemini não gerou nenhum conteúdo")

        transcript_analysed = TranscriptAnalyse.model_validate_json(response.output_text)

        return ResponseModel(
                status=status.HTTP_200_OK,
                message=transcript_analysed,
                is_valid=True
            )
    except Exception as ex:
        print(ex)
        return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                message="Ocorreu um erro inesperado"
            )

async def send_message(user_message: str, previous_interaction_id: str | None = None):
    pass

async def generate_feedback(transcript: str, tone: _FEEDBACK_TONES):
    pass

async def generate_prediction(last_transcript: str):
    pass

def _create_simple_interactor(request: str, context: str):
    prompt = f'Analise a seguinte transcricao de reuniao e retorne o JSON estruturado conforme instruido:\n\n{request}'
    return __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=prompt,
        generation_config={
            "thinking_level": "medium",
            "temperature": 0.2,

        },
        response_format={
            "type": "OBJECT",
            "mime_type": "application/json",
            "schema": TranscriptAnalyse.model_json_schema()
        },
        system_instruction=context,
        store=False
    )

def _create_complex_interactor(model: __InteractionCreateModel):
    return __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=model.request,
        previous_interaction_id=model.interaction_id,
        generation_config={
            "thinking-level": "medium",
        },
        store=True
    )
