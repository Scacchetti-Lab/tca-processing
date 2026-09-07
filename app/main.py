from fastapi import FastAPI, Request, Depends
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import APIKeyHeader
from sentence_transformers import SentenceTransformer
from app.routers import chats, embed, transcripts
from starlette.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from app.exceptions.exceptions import validation_exception_handler, custom_http_exception_handler
from app import deps
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.middleware import app_middleware
from dotenv import load_dotenv
from os import getenv

load_dotenv()

allowed_host = getenv("AI_ALLOWED_HOST") or ""
api_key_header = APIKeyHeader(name="X-ACCESS-KEY", auto_error=False)


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

@app.middleware("http")
async def middleware(request: Request, call_next):
    return await app_middleware(request, call_next)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)

app.add_middleware(GZipMiddleware, minimum_size=1000)  # comprime respostas acima de 1KB
#app.add_middleware(TrustedHostMiddleware, allowed_hosts=[allowed_host])

@app.get("/")
@app.get("/health")
def root():
    return {"status": "Ok", "project": "AI Totvs Commercial (tca-processing)", "version": "1.0.0"}

app.include_router(transcripts.router, prefix="/v1/transcript", tags=["Transcript Routes"], dependencies=[Depends(api_key_header)])
app.include_router(chats._router, prefix="/v1/chat", tags=["AI Chat Routes"], dependencies=[Depends(api_key_header)])
app.include_router(embed._router, prefix="/v1/embed", tags=["Embedding Routes"], dependencies=[Depends(api_key_header)])