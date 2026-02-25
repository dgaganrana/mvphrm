"""
System endpoints for health checks and logging
"""
from fastapi import APIRouter, Request, Body
from app.core.logging import app_logger
from typing import Any

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    app_logger.debug("Health check requested")
    return {"status": "ok"}


@router.post("/api/logs")
async def receive_frontend_logs(log_entry: dict = Body(...)):
    """Receive logs from frontend for centralized aggregation"""
    try:
        # Forward frontend logs to backend logger
        level = log_entry.get("level", "info").lower()
        message = log_entry.get("message", "Frontend log")
        
        if level == "error":
            app_logger.error(f"[Frontend] {message}", extra=log_entry)
        elif level == "warn":
            app_logger.warning(f"[Frontend] {message}", extra=log_entry)
        elif level == "debug":
            app_logger.debug(f"[Frontend] {message}", extra=log_entry)
        else:
            app_logger.info(f"[Frontend] {message}", extra=log_entry)
            
        return {"success": True}
    except Exception as e:
        app_logger.error(f"Failed to process frontend log: {str(e)}")
        return {"success": False, "error": str(e)}
