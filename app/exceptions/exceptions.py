from main import app
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc: StarletteHTTPException):
    print(f"\033[1;31m[ERRO {exc.status_code}] Falha durante inesperada durante a requisição: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    print(f"\033[1;31m[ERRO] Falha na tratativa dos dados enviados pelo body: {exc}\033[m")
    return await request_validation_exception_handler(request, exc)
