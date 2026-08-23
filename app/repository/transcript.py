from .interface.transcript import TranscriptInterface
from app.models.transcript import transcript_chunk

class TranscriptRepository(TranscriptInterface):
    def get_by_id(self, transcript_id: str):
        try:
            pass
        except Exception as ex:
            print(ex)

    def save_chunks(self, chunk_model: transcript_chunk):
        pass