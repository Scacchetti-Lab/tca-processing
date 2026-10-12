from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID
from app.types.response_model import RespositoryModel

if TYPE_CHECKING:
    from app.models.transcript import transcript_chunks



class TranscriptInterface(ABC):
    @abstractmethod
    def get_by_id(self, transcript_id: UUID) -> RespositoryModel:
        pass

    @abstractmethod
    def save_chunks(self, chunk_models: list['transcript_chunks']) -> RespositoryModel:
        pass

    @abstractmethod
    def search_simmiliarities(self, embedding_prompt: list[float]) -> RespositoryModel:
        pass