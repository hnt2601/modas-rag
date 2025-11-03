"""
FastAPI application entry point.

This module sets up the FastAPI application with all middleware,
routers, and exception handlers.
"""

from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from core.config import settings
from models.schemas import HealthCheck, ErrorResponse
from utils.logger import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    
    Handles startup and shutdown logic.
    """
    # Startup
    logger.info("🚀 Starting RAG System Backend")
    logger.info(f"Environment: {settings.log_level}")
    logger.info(f"Qdrant: {settings.qdrant_host}:{settings.qdrant_port}")
    logger.info(f"Embedding Model: {settings.embedding_model}")
    logger.info(f"LLM Model: {settings.llm_model}")
    
    # TODO: Initialize connections to Qdrant, Redis, etc.
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down RAG System Backend")
    # TODO: Close connections


# Initialize FastAPI app
app = FastAPI(
    title="RAG System API",
    description="Production-ready RAG system with Vietnamese AI models from FPT Cloud",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: The request that caused the error
        exc: The exception that was raised
        
    Returns:
        JSON response with error details
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    error_response = ErrorResponse(
        error="InternalServerError",
        message="Đã xảy ra lỗi. Vui lòng thử lại sau.",
        detail=str(exc) if settings.log_level == "DEBUG" else None
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )


# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get(
    "/health",
    response_model=HealthCheck,
    tags=["Health"],
    summary="Health check endpoint"
)
async def health_check() -> HealthCheck:
    """
    Check the health status of the application and its dependencies.
    
    Returns:
        HealthCheck: Health status of all services
    """
    checks: Dict[str, str] = {
        "api": "ok",
    }
    
    # TODO: Add checks for Qdrant, Redis, FPT Cloud API
    # For now, we'll just check the API itself
    
    try:
        # Check Qdrant connection
        # qdrant_status = await check_qdrant()
        # checks["qdrant"] = qdrant_status
        checks["qdrant"] = "not_configured"
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        checks["qdrant"] = "error"
    
    try:
        # Check FPT Cloud API
        # fpt_status = await check_fpt_cloud()
        # checks["fpt_cloud"] = fpt_status
        checks["fpt_cloud"] = "not_configured"
    except Exception as e:
        logger.error(f"FPT Cloud health check failed: {e}")
        checks["fpt_cloud"] = "error"
    
    # Determine overall status
    all_healthy = all(v == "ok" for v in checks.values() if v != "not_configured")
    status = "healthy" if all_healthy else "degraded"
    
    logger.info(f"Health check completed: {status}")
    
    return HealthCheck(
        status=status,
        checks=checks
    )


# ============================================================================
# API Routers
# ============================================================================

# TODO: Include routers when they are implemented
# from api import chat, documents
# app.include_router(chat.router, prefix="/chat", tags=["Chat"])
# app.include_router(documents.router, prefix="/documents", tags=["Documents"])


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """
    Root endpoint with API information.
    
    Returns:
        API information and version
    """
    return {
        "name": "RAG System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )

