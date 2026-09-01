
from uuid import UUID
from .interface.transcript import TranscriptInterface
from app.types.response_model import RespositoryModel
from typing import TYPE_CHECKING
from sqlmodel import select
from app.models.transcript import transcript_chunks, transcript
from app.db_connect import SessionDep

if TYPE_CHECKING:
    pass

class TranscriptRepository(TranscriptInterface):

    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_by_id(self, transcript_id: UUID) -> RespositoryModel:
        try:
            transcription = self.session.get(transcript, transcript_id)

            if not transcription:
                return RespositoryModel(message='Nenhuma transcrição encontrada com esse ID')

            return RespositoryModel(
                is_valid=True,
                message='Transcrição encontrada!',
                result=transcription
            )
        except Exception as ex:
            print(ex)
            raise ex

    def save_chunks(self, chunk_models: list['transcript_chunks']) -> RespositoryModel:
        try:
            self.session.add_all(chunk_models)

            return RespositoryModel(
                is_valid=True,
                message=f'{len(chunk_models)} chunks foram adiconados a transcript_chunks',
                result=None
            )
        except Exception as ex:
            print(ex)
            return RespositoryModel(
                message=f'Ocorreu um erro durante o INSERT\nNenhum valor foi adicionado a transcript_chunks'
            )
    def search_simmiliarities(self, embedding_prompt: list[float]) -> RespositoryModel:
        try:
            query = select(transcript_chunks).order_by(
                transcript_chunks.embedding.cosine_distance(embedding_prompt)  # type: ignore[reportAttributeAccessIssue]
            ).limit(5)

            chunks = self.session.exec(query).all()

            if not chunks:
                return RespositoryModel(message='Nenhum trecho encontrado para essa transcrição')

            return RespositoryModel(
                is_valid=True,
                message='Trechos encontrados!',
                result=chunks
            )
        except Exception as ex:
            print(ex)
            return RespositoryModel(
                message=f'Nenhuma similaridade foi encontrada nas transcrições'
            )