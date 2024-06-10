from starlette.responses import JSONResponse
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class IngestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "An internal server error occurred"}
            )
