from abc import ABC, abstractmethod
from uuid import UUID
from app.models.client import clients
from app.models.meeting import meetings
from app.types.predict_models import MeetingStrategicDto, MeetingPerformanceDto



class MeetingInterface(ABC):
    @abstractmethod
    def find_meeting_client(self, meeting_id: UUID) -> clients:
        pass

    @abstractmethod
    def get_performance_history(self, cl_id: UUID) -> list[MeetingPerformanceDto]:
        pass

    @abstractmethod
    def get_strategic_history(self, cl_id: UUID) -> list[MeetingStrategicDto]:
        pass
