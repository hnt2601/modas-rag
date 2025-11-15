"""
Configuration management using Pydantic Settings.

This module handles all application configuration from environment variables.
"""

from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be configured via .env file or environment variables.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # FPT Cloud API
    fpt_api_key: str = Field(..., description="FPT Cloud API Key")
    fpt_api_base: str = Field(
        default="https://mkp-api.fptcloud.com/v1",
        description="FPT Cloud Marketplace API Base URL"
    )
    
    # Qdrant Configuration
    qdrant_host: str = Field(default="localhost", description="Qdrant host")
    qdrant_port: int = Field(default=6333, description="Qdrant port")
    qdrant_collection_name: str = Field(
        default="documents",
        description="Qdrant collection name"
    )
    
    # Redis Configuration (Optional)
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")
    
    # Application Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    max_upload_size: int = Field(
        default=52428800,
        description="Max file upload size in bytes (50MB)"
    )
    allowed_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated CORS allowed origins"
    )
    
    # RAG Configuration
    chunk_size: int = Field(default=1000, description="Text chunk size")
    chunk_overlap: int = Field(default=200, description="Text chunk overlap")
    retrieval_top_k: int = Field(
        default=20,
        description="Number of documents to retrieve initially"
    )
    rerank_top_n: int = Field(
        default=5,
        description="Number of documents after reranking"
    )
    
    # Model Configuration
    embedding_model: str = Field(
        default="Vietnamese_Embedding",
        description="Embedding model name"
    )
    embedding_dimensions: int = Field(
        default=1024,
        description="Embedding vector dimensions"
    )
    llm_model: str = Field(default="GLM-4.5", description="LLM model name")
    llm_temperature: float = Field(default=0.7, description="LLM temperature")
    llm_max_tokens: int = Field(
        default=2000,
        description="LLM max tokens per response"
    )
    reranker_model: str = Field(
        default="bge-reranker-v2-m3",
        description="Reranker model name"
    )
    reranker_provider: str = Field(
        default="fpt",
        description="Reranker provider (fpt, cohere, jina, etc.)"
    )
    guard_model: str = Field(
        default="Llama-Guard-3-8B",
        description="Safety guard model name"
    )
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v_upper
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins to list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def fpt_config(self) -> dict:
        """Get FPT Cloud API configuration for LangChain."""
        return {
            "openai_api_key": self.fpt_api_key,
            "openai_api_base": self.fpt_api_base
        }


# Global settings instance
settings = Settings()

