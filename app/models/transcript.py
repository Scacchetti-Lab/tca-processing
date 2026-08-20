from sqlmodel import SQLModel, Field
from uuid import UUID


class Transcript(SQLModel, table=True):
    trs_id: UUID = Field(primary_key=True)
