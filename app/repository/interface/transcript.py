from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.transcript import transcript_chunk
    from app.types.response_model import RespositoryModel



class TranscriptInterface(ABC):
    @abstractmethod
    def get_by_id(self, transcript_id: str) -> RespositoryModel:
        pass

    @abstractmethod
    def save_chunks(self, chunk_models: list['transcript_chunk']) -> RespositoryModel:
        pass
