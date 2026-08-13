from fastapi import FastAPI
from app.routers import chats, transcripts
from starlette.middleware.gzip import GZipMiddleware
from middleware import app_middleware

app = FastAPI(
    title="Totvs Commercial AI - Processing",
    version="1"
)
app.add_middleware(GZipMiddleware, minimum_size=1000)  # comprime respostas acima de 1KB
# app.add_middleware(app_middleware)

@app.get("/")
def root():
    return {"status": "Ok", "project": "Totvs Commercial AI - Processing", "version": "1.0.0"}

app.include_router(transcripts.router, prefix="/v1/transcript", tags=["Transcript Routes"])
app.include_router(chats.router, prefix="/v1/chat", tags=["AI Chat Routes"])