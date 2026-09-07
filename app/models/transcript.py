from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from uuid import UUID, uuid4
from pgvector.sqlalchemy import Vector
from app.constants.transcript import TRANSCRIPT_DB_STATUS
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.meeting import meetings


class transcripts(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4,primary_key=True, index=True)
    raw_transcript: str
    resume: str
    status: TRANSCRIPT_DB_STATUS = Field(sa_column=Column(String(255), nullable=False), default='NOT_STARTED')

    transcript_chunks: list["transcript_chunks"] = Relationship(back_populates='transcript')
    meeting: 'meetings' = Relationship(back_populates='transcript')

class transcript_chunks(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    chunk_text: str
    created_at: datetime
    embedding: list[float] = Field(sa_column=Column(Vector(384), nullable=False))

    transcript_id: UUID = Field(foreign_key='transcripts.id')
    transcript: transcripts = Relationship(back_populates='transcript_chunks')