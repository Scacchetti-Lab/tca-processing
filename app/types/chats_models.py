from uuid import UUID
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Literal

class InteractionCreateModel(BaseModel):
    request: str
    interaction_id: str | None

class ChatBotResponse(BaseModel):
    title: str | None = None
    reply: str
    previous_interaction_id: str | None = None
    tokens_used: int = 0

class MeetingPredictRequest(BaseModel):
    meeting_id: UUID

class ClientPredictRequest(BaseModel):
    client_id: UUID

class ChatMessagesResponse(BaseModel):
    message: str
    previous_interact_id: str | None = None
    chat_model: Literal["VOICE", "TEXT"] = "TEXT"


@dataclass
class TextChunk:
    text: str

@dataclass
class TitleReady:
    title: str

@dataclass
class InteractionCreated:
    interaction_id: str