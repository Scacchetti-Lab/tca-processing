from os import getenv
from dotenv import load_dotenv
from google import genai
from constants.ai_context import FEEDBACK_TONES
from models.chats_models import InteractionCreateModel

load_dotenv()

GEMINI_API_KEY = getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = getenv("GEMINI_MODEL_NAME")

client = genai.Client(api_key=GEMINI_API_KEY)

async def analyse_transcript(transcript: str):
    pass

async def send_message(user_message: str, previous_interaction_id: str | None = None):
    pass

async def generate_feedback(transcript: str, tone: FEEDBACK_TONES):
    pass

async def generate_prediction(last_transcript: str):
    pass


def create_interactor(model: InteractionCreateModel):
    return client.interactions.create(
        model=GEMINI_MODEL_NAME,
        input=model.request,
        previous_interaction_id=model.interaction_id,
        generation_config={
            "thinking-level": "high" if model.isChatting else "medium",
        },
        store=True
    )