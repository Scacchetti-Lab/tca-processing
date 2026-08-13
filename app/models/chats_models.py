from pydantic import BaseModel

class InteractionCreateModel(BaseModel):
    request: str
    interaction_id: str | None
