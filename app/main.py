from fastapi import FastAPI
from app.routers import chats, transcripts

app = FastAPI(
    title="Totvs Commercial AI - Processing",
    version="1"
)

@app.get("/")
def root():
    return {"status": "Ok", "project": "Totvs Commercial AI - Processing", "version": "1.0.0"}

app.include_router(transcripts.router, prefix="/v1/transcript", tags=["Transcript Routes"])
app.include_router(chats.router, prefix="/v1/chat", tags=["AI Chat Routes"])