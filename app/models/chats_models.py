from pydantic import BaseModel

class InteractionCreateModel(BaseModel):
    request: str
    interaction_id: str
    isChatting: bool # Usado para Transcrições e Feedbacks, no chat convencional deve ser false
