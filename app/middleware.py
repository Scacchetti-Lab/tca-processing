import secrets
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
from os import getenv

from fastapi.responses import JSONResponse

load_dotenv()

secret_key = getenv("AI_SECRET_KEY")

async def app_middleware(request: Request, call_next) -> JSONResponse:
    if request.url.path in ("/", "/health", "/docs", "/openapi.json"):
        return await call_next(request)

    if not request.headers.get("X-ACCESS-KEY"):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            content={"detail":"Acesso Negado"}
        )

    token = request.headers["X-ACCESS-KEY"]
    if not token or not secret_key or not secrets.compare_digest(token, secret_key):
        return JSONResponse(
            status_code=403,
            content={"detail": "Credencial incorreta"}
        )

    return await call_next(request)