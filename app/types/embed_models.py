from pydantic import BaseModel

class ChunkRequets(BaseModel):
    transcript_id: str

class ClientEmbedd(BaseModel):
    client_id: str

class MeetingEmbedd(BaseModel):
    meeting_id: str