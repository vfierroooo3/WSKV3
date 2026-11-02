from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def exception_handler(request: Request, exc: Exception):
    headers = None

    if isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        message = str(exc.detail)
        headers = exc.headers

    elif isinstance(exc, DuplicateKeyError):
        status_code = 409
        message = "Project already exists or another unique field conflicts"

    elif isinstance(exc, RequestValidationError):
        status_code = 422
        message = "Invalid input data"

    else:
        status_code = 500
        message = "Unable to process request"

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "errorMessage": message
        },
        headers=headers
    )


def register_exception_handlers(app: FastAPI):
    for exception_type in (
        StarletteHTTPException,
        RequestValidationError,
        DuplicateKeyError,
        Exception
    ):
        app.add_exception_handler(
            exception_type,
            exception_handler
        )