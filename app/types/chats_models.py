from pydantic import BaseModel

class InteractionCreateModel(BaseModel):
    request: str
    interaction_id: str | None

class ChatBotResponse(BaseModel):
    user_input: str
    answer: str
    previous_interaction_id: str | None