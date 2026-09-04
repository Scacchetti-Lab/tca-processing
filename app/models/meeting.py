from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS, INSIGHT_PRIORITY
from datetime import datetime
from typing import Literal

if TYPE_CHECKING:
    from models.client import client
    from models.transcript import transcript

class meeting(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    totvs_id: int | None = Field(unique=True, index=True)
    title: str = Field(unique=True)
    duration_min: int
    summary: str | None = Field(default=None, nullable=True)
    scheduled: datetime
    status: Literal['SCHEDULED', 'IN_PROGRESS' 'CANCELLED', 'COMPLETED'] = Field(sa_column=Column(String(255), nullable=False), default='SCHEDULED')
    performance_avg: float | None = Field(default=None, nullable=True) # Porcentagem do desempenho da reunião
    feedback: str
    priority: INSIGHT_PRIORITY | None = Field(sa_column=Column(String(255), nullable=True), default=None)
    is_deleted: bool = Field(default=False)
    embeddings: list[float] | None = Field(default=None, sa_column=Column(Vector(384), nullable=True))

    transcript_id: UUID = Field(foreign_key='transcript.id', unique=True, index=True)
    transcript: 'transcript' = Relationship(back_populates='meeting')

    client_id: UUID = Field(foreign_key='client.id', nullable=False)
    client: 'client' = Relationship(back_populates='meetings')

    strategic_analyse: 'meeting_strategic_analyse' = Relationship(back_populates='meeting')
    performance_analyse: 'meeting_performance_analyse' = Relationship(back_populates='meeting')

    strategic_analyse: 'meeting_strategic_analyse' = Relationship(back_populates='meeting')
    performance_analyse: 'meeting_performance_analyse' = Relationship(back_populates='meeting')
    employees: list['meeting_employee'] = Relationship(back_populates='meeting')

class meeting_employee(SQLModel, table=True):
    __table_args__ = (UniqueConstraint('meeting_id', 'user_profile_id'),)

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    feedback_tip: str

    meeting_id: UUID = Field(foreign_key='meeting.id', index=True)
    meeting: meeting = Relationship(back_populates='employees')

    user_profile_id: UUID = Field(foreign_key='user_profile.up_id', index=True)

class meeting_strategic_analyse(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    employees_performance: float
    company_status: COMPANY_STATUS = Field(sa_column=Column(String(255), nullable=False))
    company_performance: float
    closing_probability: float
    problem_understanding: float
    risk: float
    financial_impact: float
    financial_impact_status: FINANCIAL_STATUS = Field(sa_column=Column(String(255), nullable=False))
    created_at: datetime = Field(default_factory=datetime.now)

    meeting_id: UUID = Field(foreign_key='meeting.id', unique=True, index=True)
    meeting: meeting = Relationship(back_populates='strategic_analyse')

    client_id: UUID = Field(foreign_key='client.id', index=True)
    client: 'client' = Relationship(back_populates='strategic_analyses')


class meeting_performance_analyse(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    engagement: float
    opportunities_seized: float
    communication_quality: float
    objection_handling: float
    converted_potencials: float
    leads_converted: int
    tips: str
    created_at: datetime = Field(default_factory=datetime.now)

    meeting_id: UUID = Field(foreign_key='meeting.id', unique=True, index=True)
    meeting: meeting = Relationship(back_populates='performance_analyse')