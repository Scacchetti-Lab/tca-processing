from abc import ABC, abstractmethod

class TranscriptInterface(ABC):
    @abstractmethod
    def get_by_id(self, transcript_id: str):
        pass

    @abstractmethod
    def save_chunks(self, chunk_model):
        pass
