from fastapi import FastAPI, Depends
from sentence_transformers import SentenceTransformer
from app.routers import chats, embed, transcripts
from starlette.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from app.exceptions.exceptions import validation_exception_handler, custom_http_exception_handler
from app import deps
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
# from middleware import app_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    deps.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    yield
    deps.model = None


app = FastAPI(
    title="Totvs Commercial AI - Processing",
    version="1",
    lifespan=lifespan
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)

app.add_middleware(GZipMiddleware, minimum_size=1000)  # comprime respostas acima de 1KB
# app.add_middleware(app_middleware)

@app.get("/")
@app.get("/health-check")
def root():
    return {"status": "Ok", "project": "Totvs Commercial AI - Processing", "version": "1.0.0"}

app.include_router(transcripts.router, prefix="/v1/transcript", tags=["Transcript Routes"])
app.include_router(chats._router, prefix="/v1/chat", tags=["AI Chat Routes"])
app.include_router(embed._router, prefix="/v1/embed", tags=["Embedding Routes"])