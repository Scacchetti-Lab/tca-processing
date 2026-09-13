from uuid import UUID
from sqlmodel import select, col
from app.models.client import client_analysis, clients
from app.models.meeting import meeting_strategic_analyses
from app.db_connect import SessionDep as __SessionDep

from app.repository.interface.client import ClientInterface
from app.types.predict_models import MeetingStrategicDto


class ClientRepository(ClientInterface): 
    def __init__(self, session: __SessionDep):
        self.session = session

    def find_by_id(self, id: UUID) -> clients | None:
        return self.session.exec(select(clients).where(clients.id == id)).one_or_none()

        
    def find_client_details(self, id: UUID):
        statement = (
            select(client_analysis)
            .where(client_analysis.client_id == id)
        )
        return self.session.exec(statement).one_or_none()