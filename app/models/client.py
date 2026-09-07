from sqlmodel import SQLModel, Relationship, Field
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS
from uuid import UUID, uuid4
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
    
    embeddings: list[float] = Field(sa_column=Column(Vector(384), nullable=False))

    meetings: list['meetings'] = Relationship(back_populates='client')
    client_analyse: 'client_analyses' = Relationship(back_populates='client')
    strategic_analyses: list['meeting_strategic_analyses'] = Relationship(back_populates='client')

class client_analyses(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    performance: int | None = Field(default=None, decimal_places=1)
    closing_probability: int | None = Field(default=None, decimal_places=1)
    problem_understanding: int | None = Field(default=None, decimal_places=1)
    risk: int | None = Field(default=None)
    financial_impact: float | None = Field(default=None, decimal_places=2)
    financial_status: FINANCIAL_STATUS | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    client_id: UUID = Field(foreign_key='clients.id', unique=True)
    client: clients = Relationship(back_populates='client_analyse')