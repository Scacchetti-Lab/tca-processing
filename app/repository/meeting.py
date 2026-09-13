from uuid import UUID
from sqlmodel import select, col
from app.db_connect import SessionDep
from app.repository.interface.meeting import MeetingInterface
from app.types.predict_models import MeetingPerformanceDto, MeetingStrategicDto
from app.models.meeting import meetings, meeting_performance_analyses as mpa, meeting_strategic_analyses as msa

class MeetingRepository(MeetingInterface):
    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def find_meeting_client(self, meeting_id: UUID):
        statement = select(meetings).where(meetings.id == meeting_id)
        meeting = self.session.exec(statement).one_or_none()
        if meeting is None:
            raise ValueError("ID da reunião informado é inválido")

        return meeting.client

    def get_performance_history(self, cl_id: UUID) -> list[MeetingPerformanceDto]:
        statement = (
            select(mpa)
            .join(meetings)
            .where(meetings.client_id == cl_id)
            .order_by(col(meetings.scheduled).asc())
        )
        analyses = self.session.exec(statement).all()

        return [
            MeetingPerformanceDto(
                communication_quality=an.communication_quality,
                engagement=an.engagement,
                feedback=an.feedback,
                tips=an.tips,
                missed_opportunities=an.missed_opportunities,
                objection_handling=an.objection_handling,
                opportunities_seized=an.opportunities_seized,
            )
            for an in analyses
        ]

    def get_strategic_history(self, cl_id: UUID):
        statement = (
            select(msa)
            .join(meetings)
            .where(meetings.client_id == cl_id)
            .order_by(col(meetings.scheduled).asc())
        )
        analyses = self.session.exec(statement)

        return [
            MeetingStrategicDto(
                tips=an.tips,
                feedback=an.feedback,
                closing_probability=an.closing_probability,
                financial_impact=an.financial_impact_value,
                financial_impact_status=an.financial_impact_status,
                flexibility=an.flexibility,
                risk=an.risk
            )
            for an in analyses
        ]