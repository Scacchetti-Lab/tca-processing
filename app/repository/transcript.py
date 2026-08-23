
from uuid import UUID
from .interface.transcript import TranscriptInterface
from app.types.response_model import RespositoryModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.transcript import transcript_chunk, transcript
    from app.db_connect import SessionDep

class TranscriptRepository(TranscriptInterface):

    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_by_id(self, transcript_id: UUID) -> RespositoryModel:
        try:
            transcription = self.session.get_one(transcript, transcript_id)

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

    def save_chunks(self, chunk_models: list['transcript_chunk']) -> RespositoryModel:
        try:
            self.session.add_all(chunk_models)

            return RespositoryModel(
                is_valid=True,
                message=f'{len(chunk_models)} valores foram adiconados a {transcript_chunk.__str__}',
                result=chunk_models
            )
        except Exception as ex:
            print(ex)
            return RespositoryModel(
                message=f'Ocorreu um erro durante o INSERT\nNenhum valor foi adicionado a {transcript_chunk.__str__}'
            )