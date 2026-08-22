from sqlmodel import SQLModel, Relationship, Field
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS
from .meeting import meeting
from uuid import UUID, uuid4
from typing import Literal

class client(SQLModel, table=True):
    cl_id: UUID = Field(default_factory=uuid4, primary_key=True)
    cl_name: str
    cl_fantasy_name: str
    cl_cnpj: str = Field(max_length=14, unique=True)
    cl_addres_id: UUID
    cl_revenue: float = Field(decimal_places=2)
    cl_status: COMPANY_STATUS
    cl_embeddings: list[float] = Field(sa_column=Column(Vector(384), nullable=False))

    cl_meetings: list['meeting'] = Relationship(back_populates='client')

class client_analyse(SQLModel, table=True):
    ca_id: UUID = Field(default_factory=uuid4, primary_key=True)
    ca_performance: int | None = Field(default=None, decimal_places=1)
    ca_closing_probability: int | None = Field(default=None, decimal_places=1)
    ca_problem_understanding: int | None = Field(default=None, decimal_places=1)
    ca_risk: int | None = Field(default=None)
    ca_financial_impact: float | None = Field(default=None, decimal_places=2)
    ca_financial_status: FINANCIAL_STATUS | None = Field(default=None)
    ca_embeddings: list[float] = Field(sa_column=Column(Vector(384), nullable=False))
    
    ca_client_id: UUID = Field(foreign_key='client.cl_id', unique=True)
    ca_client: client = Relationship(back_populates='cl_client_analyse')