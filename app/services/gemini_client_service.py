from os import getenv as __getenv
from dotenv import load_dotenv as __load_dotenv
from google import genai as __genai
from constants.ai_context import FEEDBACK_TONES as __FEEDBACK_TONES
from models.chats_models import InteractionCreateModel as __InteractionCreateModel
from models.transcripts_models import TranscriptAnalyse as __TranscriptAnalyse

__load_dotenv()

__GEMINI_API_KEY = __getenv("GEMINI_API_KEY")
__GEMINI_MODEL_NAME = __getenv("GEMINI_MODEL_NAME")

__client = __genai.Client(api_key=__GEMINI_API_KEY)

async def analyse_transcript(transcript: str) -> __TranscriptAnalyse | None:
    pass

async def send_message(user_message: str, previous_interaction_id: str | None = None):
    pass

async def generate_feedback(transcript: str, tone: __FEEDBACK_TONES):
    pass

async def generate_prediction(last_transcript: str):
    pass


def __create_interactor(model: __InteractionCreateModel):
    return __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=model.request,
        previous_interaction_id=model.interaction_id,
        generation_config={
            "thinking-level": "high" if model.isChatting else "medium",
        },
        store=True
    )