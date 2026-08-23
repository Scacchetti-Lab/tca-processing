from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.models.transcript import transcript_chunks
    from app.types.response_model import RespositoryModel



class TranscriptInterface(ABC):
    @abstractmethod
    def get_by_id(self, transcript_id: UUID) -> RespositoryModel:
        pass

    @abstractmethod
    def save_chunks(self, chunk_models: list['transcript_chunks']) -> RespositoryModel:
        pass
