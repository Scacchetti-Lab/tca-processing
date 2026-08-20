from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from app.models import client
from .transcript import transcript
from .client import client
from datetime import datetime
from typing import Literal

class meeting(SQLModel, table=True):
    mt_id: UUID = Field(default_factory=uuid4, primary_key=True)
    mt_totvs_id: int | None = Field(unique=True, index=True)
    mt_title: str = Field(unique=True)
    mt_datetime: str = Field(default_factory=datetime.now)
    mt_summary: str | None = Field(default=None, nullable=True)
    mt_scheduled: str | datetime
    mt_status: Literal['SCHEDULED', 'CANCELLED', 'COMPLETED', 'RESCHEDULED'] = Field(default='SCHEDULED')
    mt_performance: float | None = Field(default=None, nullable=True) # Porcentagem do desempenho da reunião
    mt_is_deleted: bool = Field(default=False)
    mt_embeddings: list[float] = Field(sa_column=Column(Vector(384), nullable=False))

    mt_transcript_id: UUID = Field(foreign_key='transcript.tr_id', unique=True, index=True)
    mt_transcript: transcript = Relationship(back_populates='tr_meeting')

    mt_client_id: UUID = Field(foreign_key='client.cl_id')
    mt_client: client = Relationship(back_populates='cl_meetings')
