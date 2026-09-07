from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS, INSIGHT_PRIORITY
from datetime import datetime
from typing import Literal

if TYPE_CHECKING:
    from models.client import clients
    from models.transcript import transcripts

class meetings(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    totvs_id: int | None = Field(unique=True, index=True)
    title: str = Field(unique=True)
    duration_min: int
    summary: str | None = Field(default=None, nullable=True)
    scheduled: datetime
    status: Literal['SCHEDULED', 'IN_PROGRESS' 'CANCELLED', 'COMPLETED'] = Field(sa_column=Column(String(255), nullable=False), default='SCHEDULED')
    performance_avg: float | None = Field(default=None, nullable=True) # Porcentagem do desempenho da reunião
    priority: INSIGHT_PRIORITY | None = Field(sa_column=Column(String(255), nullable=True), default=None)
    is_deleted: bool = Field(default=False)
    embeddings: list[float] | None = Field(default=None, sa_column=Column(Vector(384), nullable=True))
    client_representor: str

    transcript_id: UUID = Field(foreign_key='transcripts.id', unique=True, index=True)
    transcript: 'transcripts' = Relationship(back_populates='meeting')

    client_id: UUID = Field(foreign_key='clients.id', nullable=False)
    client: 'clients' = Relationship(back_populates='meetings')

    strategic_analyse: 'meeting_strategic_analyses' = Relationship(back_populates='meeting')
    performance_analyse: 'meeting_performance_analyses' = Relationship(back_populates='meeting')

    strategic_analyse: 'meeting_strategic_analyses' = Relationship(back_populates='meeting')
    performance_analyse: 'meeting_performance_analyses' = Relationship(back_populates='meeting')
    employees: list['meeting_employees'] = Relationship(back_populates='meeting')

class meeting_employees(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    feedback_tip: str

    meeting_id: UUID = Field(foreign_key='meetings.id', index=True)
    meeting: meetings = Relationship(back_populates='employees')
    user_id: UUID

class meeting_strategic_analyses(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    company_status: COMPANY_STATUS = Field(sa_column=Column(String(255), nullable=False))
    company_performance: float
    closing_probability: float
    flexibility: float
    risk: float
    financial_impact: float
    financial_impact_value: float
    financial_impact_status: FINANCIAL_STATUS = Field(sa_column=Column(String(255), nullable=False))
    created_at: datetime = Field(default_factory=datetime.now)
    feedback: str

    meeting_id: UUID = Field(foreign_key='meetings.id', unique=True, index=True)
    meeting: meetings = Relationship(back_populates='strategic_analyse')

    client_id: UUID = Field(foreign_key='clients.id', index=True)
    client: 'clients' = Relationship(back_populates='strategic_analyses')


class meeting_performance_analyses(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    engagement: float
    opportunities_seized: float
    communication_quality: float
    objection_handling: float
    missed_opportunities: float
    leads_converted: int
    tips: str
    feedback: str
    created_at: datetime = Field(default_factory=datetime.now)

    meeting_id: UUID = Field(foreign_key='meetings.id', unique=True, index=True)
    meeting: meetings = Relationship(back_populates='performance_analyse')