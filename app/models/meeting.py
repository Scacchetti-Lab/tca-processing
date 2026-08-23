from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS, TRANSCRIPT_TYPE, INSIGHT_PRIORITY
from datetime import datetime
from typing import Literal

if TYPE_CHECKING:
    from models.client import client
    from models.transcript import transcript

class meeting(SQLModel, table=True):
    mt_id: UUID = Field(default_factory=uuid4, primary_key=True)
    mt_totvs_id: int | None = Field(unique=True, index=True)
    mt_title: str = Field(unique=True)
    mt_duration_meeting: datetime = Field(default_factory=datetime.now)
    mt_summary: str | None = Field(default=None, nullable=True)
    mt_scheduled: datetime
    mt_status: Literal['SCHEDULED', 'CANCELLED', 'COMPLETED', 'RESCHEDULED'] = Field(sa_column=Column(String(255), nullable=False), default='SCHEDULED')
    mt_performance_avg: float | None = Field(default=None, nullable=True) # Porcentagem do desempenho da reunião
    mt_type: TRANSCRIPT_TYPE = Field(sa_column=Column(String(255), nullable=False))
    mt_feedback: str
    mt_priority: INSIGHT_PRIORITY | None = Field(sa_column=Column(String(255), nullable=False), default=None)
    mt_is_deleted: bool = Field(default=False)
    mt_embeddings: list[float] | None = Field(default=None, sa_column=Column(Vector(384), nullable=True))

    mt_transcript_id: UUID = Field(foreign_key='transcript.tr_id', unique=True, index=True)
    mt_transcript: 'transcript' = Relationship(back_populates='tr_meeting')

    mt_client_id: UUID = Field(foreign_key='client.cl_id')
    mt_client: 'client' = Relationship(back_populates='cl_meetings')

    mt_strategic_analyse: 'meeting_strategic_analyse' = Relationship(back_populates='sa_meeting')
    mt_performance_analyse: 'meeting_performance_analyse' = Relationship(back_populates='pa_meeting')

class meeting_employee(SQLModel, table=True):
    __table_args__ = (UniqueConstraint('me_meeting_id', 'me_user_profile_id'),)

    me_id: UUID = Field(default_factory=uuid4, primary_key=True)
    me_feedback_tip: str

    me_meeting_id: UUID = Field(foreign_key='meeting.mt_id', index=True)
    me_meeting: meeting = Relationship(back_populates='mt_employees')

    me_user_profile_id: UUID = Field(foreign_key='user_profile.up_id', index=True)

class meeting_strategic_analyse(SQLModel, table=True):
    sa_id: UUID = Field(default_factory=uuid4, primary_key=True)
    sa_employees_performance: float
    sa_company_status: COMPANY_STATUS = Field(sa_column=Column(String(255), nullable=False))
    sa_company_performance: float
    sa_closing_probability: float
    sa_problem_understanding: float
    sa_risk: float
    sa_financial_impact: float
    sa_financial_impact_status: FINANCIAL_STATUS = Field(sa_column=Column(String(255), nullable=False))
    sa_created_at: datetime = Field(default_factory=datetime.now)

    sa_meeting_id: UUID = Field(foreign_key='meeting.mt_id', unique=True, index=True)
    sa_meeting: meeting = Relationship(back_populates='mt_strategic_analyse')

    sa_client_id: UUID = Field(foreign_key='client.cl_id', index=True)
    sa_client: 'client' = Relationship(back_populates='cl_strategic_analyses')


class meeting_performance_analyse(SQLModel, table=True):
    pa_id: UUID = Field(default_factory=uuid4, primary_key=True)
    pa_engagement: float
    pa_opportunities_seized: float
    pa_communication_quality: float
    pa_objection_handling: float
    pa_converted_potencials: float
    pa_leads_converted: int
    pa_tips: str
    pa_created_at: datetime = Field(default_factory=datetime.now)

    pa_meeting_id: UUID = Field(foreign_key='meeting.mt_id', unique=True, index=True)
    pa_meeting: meeting = Relationship(back_populates='mt_performance_analyse')