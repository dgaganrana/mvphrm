"""
FastAPI middleware for logging requests and responses
"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from app.core.logging import api_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses with correlation IDs"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or retrieve correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        # Log request
        start_time = time.time()
        
        request_body = ""
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                request_body = await request.body()
                # Reset request body for actual processing
                async def receive():
                    return {"type": "http.request", "body": request_body}
                request._receive = receive
            except Exception:
                pass

        api_logger.info(
            f"Request started",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration = time.time() - start_time
            api_logger.error(
                f"Request failed with exception",
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration * 1000,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                }
            )
            raise

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        # Log response
        duration = time.time() - start_time
        api_logger.info(
            f"Request completed",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration * 1000,
                "response_size": response.headers.get("content-length", "unknown"),
            }
        )

        return response
