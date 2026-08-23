from fastapi import Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

async def custom_http_exception_handler(request: Request, exc):
    print(f"\033[1;31m[ERRO {exc.status_code}] Falha durante inesperada durante a requisição: {repr(exc)}")
    return await http_exception_handler(request, exc)

async def validation_exception_handler(request: Request, exc):
    print(f"\033[1;31m[ERRO] Falha na tratativa dos dados enviados pelo body: {exc}\033[m")
    return await request_validation_exception_handler(request, exc)
