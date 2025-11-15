"""
Reranker Factory

This module provides a factory for creating reranker service instances
based on configuration.
"""

from typing import Optional

from domain.interfaces.services.reranker_service import IRerankerService
from core.config import Settings
from infrastructure.ai.reranking.fpt_reranker_adapter import FptRerankerAdapter
from loguru import logger


class RerankerFactory:
    """
    Factory for creating reranker service instances

    This factory creates the appropriate reranker implementation based on
    the configuration. It supports multiple providers and can be extended
    easily.

    Example:
        settings = Settings()
        reranker = RerankerFactory.create(settings)

        # Use reranker
        results = await reranker.rerank(query, documents, top_n=5)
    """

    @staticmethod
    def create(
        settings: Settings,
        provider: Optional[str] = None
    ) -> IRerankerService:
        """
        Create a reranker service instance

        Args:
            settings: Application settings
            provider: Optional provider override (default: from settings)

        Returns:
            IRerankerService implementation

        Raises:
            ValueError: If provider is unknown
        """
        # Use provider from parameter or settings
        reranker_provider = provider or getattr(
            settings,
            "reranker_provider",
            "fpt"  # Default to FPT
        )

        logger.info(
            f"Creating reranker service",
            provider=reranker_provider,
            model=settings.reranker_model
        )

        if reranker_provider.lower() == "fpt":
            return FptRerankerAdapter(settings)

        # Add more providers here as needed
        # elif reranker_provider.lower() == "cohere":
        #     return CohereRerankerAdapter(settings)
        # elif reranker_provider.lower() == "jina":
        #     return JinaRerankerAdapter(settings)

        else:
            available = ["fpt"]
            raise ValueError(
                f"Unknown reranker provider: {reranker_provider}. "
                f"Available: {', '.join(available)}"
            )


# Convenience function
def create_reranker(settings: Settings) -> IRerankerService:
    """
    Convenience function to create reranker

    Args:
        settings: Application settings

    Returns:
        IRerankerService implementation
    """
    return RerankerFactory.create(settings)
