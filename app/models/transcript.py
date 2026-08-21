from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from uuid import UUID, uuid4
from pgvector.sqlalchemy import Vector
from app.constants.transcript import TRANSCRIPT_DB_STATUS
from .meeting import meeting

class transcript(SQLModel, table=True):
    tr_id: UUID = Field(default_factory=uuid4,primary_key=True)
    tr_raw_transcript: str
    tr_resume: str
    tr_status: TRANSCRIPT_DB_STATUS = Field(default='NOT_STARTED')

    tr_transcript_chunks: list["transcript_chunk"] = Relationship(back_populates='transcript')
    tr_meeting: meeting = Relationship(back_populates='transcript')

class transcript_chunk(SQLModel, table=True):
    tc_id: UUID = Field(default_factory=uuid4, primary_key=True)
    tc_chunk_text: str
    tc_embeddings: list[float] = Field(sa_column=Column(Vector(384), nullable=False))
    tc_created_at: str

    tc_transcript_id: UUID = Field(foreign_key='transcript.tr_id')
    tc_transcript: transcript = Relationship(back_populates='tr_transcript_chunks')