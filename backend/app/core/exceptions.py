from typing import Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class NurturaException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class AIProviderError(NurturaException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details,
        )


class InvalidInputError(NurturaException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NurturaException)
    async def nurtura_exception_handler(request: Request, exc: NurturaException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details,
                },
            },
        )
