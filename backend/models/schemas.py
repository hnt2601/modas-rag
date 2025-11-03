"""
Pydantic models for request/response validation.

This module defines all data models used in the API endpoints.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Health Check Models
# ============================================================================

class HealthCheck(BaseModel):
    """Health check response model."""
    
    status: str = Field(description="Overall health status")
    checks: Dict[str, str] = Field(description="Individual service checks")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Chat Models
# ============================================================================

class ChatRequest(BaseModel):
    """Chat request model."""
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's chat message"
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream the response"
    )
    
    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validate and clean message."""
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v


class ChatResponse(BaseModel):
    """Chat response model."""
    
    answer: str = Field(description="AI-generated response")
    sources: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Source documents used"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )


class StreamChunk(BaseModel):
    """Streaming response chunk model."""
    
    text: str = Field(description="Text chunk")
    done: bool = Field(default=False, description="Whether streaming is complete")


# ============================================================================
# Document Models
# ============================================================================

class DocumentMetadata(BaseModel):
    """Document metadata model."""
    
    filename: str = Field(description="Original filename")
    file_type: str = Field(description="File extension")
    file_size: int = Field(description="File size in bytes")
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    chunk_count: Optional[int] = Field(
        default=None,
        description="Number of chunks created"
    )


class DocumentUploadResponse(BaseModel):
    """Document upload response model."""
    
    document_id: str = Field(description="Unique document identifier")
    filename: str = Field(description="Original filename")
    status: str = Field(description="Processing status")
    message: str = Field(description="Status message")
    metadata: Optional[DocumentMetadata] = None


class DocumentInfo(BaseModel):
    """Document information model."""
    
    document_id: str = Field(description="Unique document identifier")
    filename: str = Field(description="Original filename")
    file_type: str = Field(description="File extension")
    file_size: int = Field(description="File size in bytes")
    chunk_count: int = Field(description="Number of chunks")
    upload_time: datetime = Field(description="Upload timestamp")


class DocumentListResponse(BaseModel):
    """Document list response model."""
    
    documents: List[DocumentInfo] = Field(description="List of documents")
    total: int = Field(description="Total number of documents")


class DocumentDeleteResponse(BaseModel):
    """Document deletion response model."""
    
    document_id: str = Field(description="Deleted document ID")
    status: str = Field(description="Deletion status")
    message: str = Field(description="Status message")


# ============================================================================
# Error Models
# ============================================================================

class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(description="Error type")
    message: str = Field(description="Error message in Vietnamese")
    detail: Optional[str] = Field(
        default=None,
        description="Additional error details"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

