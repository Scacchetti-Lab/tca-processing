from abc import ABC, abstractmethod
from uuid import UUID


class ClientInterface(ABC):
    @abstractmethod
    def find_client_status(self, id: UUID):
        pass

    @abstractmethod
    def get_all_client_analysis(self, id: UUID):
        pass
