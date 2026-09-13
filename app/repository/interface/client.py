from abc import ABC, abstractmethod
from uuid import UUID
from app.models.client import client_analysis, clients
from app.types.predict_models import MeetingStrategicDto


class ClientInterface(ABC):
    @abstractmethod
    def find_by_id(self, id: UUID) -> clients | None:
        pass

    @abstractmethod
    def find_client_details(self, id: UUID) -> client_analysis | None:
        pass
