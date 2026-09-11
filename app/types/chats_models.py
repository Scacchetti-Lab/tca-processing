from pydantic import BaseModel
from typing import Literal

class InteractionCreateModel(BaseModel):
    request: str
    interaction_id: str | None

class ChatBotResponse(BaseModel):
    reply: str
    previous_interaction_id: str | None
    tokens_used: int

class ChatBotFirstResponse(BaseModel):
    title: str | None
    reply: str
    previous_interaction_id: str | None
    tokens_used: int

class ChatPredictRequest(BaseModel):
    chat_id: str
    action: Literal['meeting', 'client']

class ChatMessagesResponse(BaseModel):
    message: str
    previous_interact_id: str | None = None