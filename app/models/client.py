from datetime import datetime

from sqlmodel import SQLModel, Relationship, Field
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String
from app.constants.transcript import COMPANY_STATUS
from uuid import uuid4, UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.meeting import meetings
    from app.models.meeting import meeting_strategic_analyses


class clients(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    fantasy_name: str
    cnpj: str = Field(max_length=14, unique=True)
    address_id: UUID
    revenue: float = Field(decimal_places=2)
    status: COMPANY_STATUS = Field(sa_column=Column(String(255), nullable=False))
    email: str
    phone: str
    
    embeddings: list[float] = Field(sa_column=Column(Vector(384), nullable=False))

    meetings: list['meetings'] = Relationship(back_populates='client')
    strategic_analyses: list['meeting_strategic_analyses'] = Relationship(back_populates='client')

class client_analysis(SQLModel, table=True):
    __tablename__ = "client_current_analysis"  # type: ignore
    client_id: UUID = Field(primary_key=True)
    performance: float | None = None
    closing_probability: float | None = None
    flexibility: float | None = None
    risk: float | None = None
    financial_impact: float | None = None
    financial_status: str | None = None
    meetings_analysed: int | None = None
    last_analysis_at: datetime | None = None