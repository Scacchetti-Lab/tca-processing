from uuid import UUID

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

class MeetingPredictRequest(BaseModel):
    meeting_id: UUID

class ClientPredictRequest(BaseModel):
    client_id: UUID

class ChatMessagesResponse(BaseModel):
    message: str
    previous_interact_id: str | None = None
    chat_model: Literal["VOICE", "TEXT"] = "TEXT"