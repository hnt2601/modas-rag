"""
FPT Cloud BGE Reranker v2-m3 Adapter

This module implements the IRerankerService interface for FPT Cloud's
BGE Reranker v2-m3 model.
"""

import httpx
from typing import List, Tuple, Dict, Any
import asyncio
from dataclasses import dataclass

from domain.interfaces.services.reranker_service import (
    IRerankerService,
    RerankResult
)
from core.config import Settings
from loguru import logger


class FptRerankerAdapter(IRerankerService):
    """
    Adapter for FPT Cloud BGE Reranker v2-m3

    This adapter uses FPT Cloud's API to rerank documents based on
    relevance to a query using the BGE Reranker v2-m3 model.

    Features:
    - Multilingual support (especially good for Vietnamese)
    - Direct similarity scoring (no embeddings)
    - Efficient re-ranking of top-k results

    Usage:
        config = Settings()
        reranker = FptRerankerAdapter(config)

        results = await reranker.rerank(
            query="What is AI?",
            documents=["AI is...", "Machine learning..."],
            top_n=5
        )
    """

    def __init__(self, settings: Settings):
        """
        Initialize FPT Reranker adapter

        Args:
            settings: Application settings with FPT API configuration
        """
        self._api_key = settings.fpt_api_key
        self._api_base = settings.fpt_api_base
        self._model = settings.reranker_model
        self._timeout = 30.0
        self._max_retries = 3

        logger.info(
            f"Initialized FPT Reranker adapter: {self._model}",
            api_base=self._api_base
        )

    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_n: int = 5
    ) -> List[RerankResult]:
        """
        Rerank documents based on relevance to query

        This method sends the query and documents to FPT Cloud's reranker API
        and returns the top_n most relevant documents with scores.

        Args:
            query: The search query
            documents: List of document texts to rerank
            top_n: Number of top results to return (default: 5)

        Returns:
            List of RerankResult ordered by relevance (highest score first)

        Raises:
            ValueError: If query is empty or documents list is empty
            RuntimeError: If API call fails after retries
        """
        # Validate inputs
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not documents:
            raise ValueError("Documents list cannot be empty")

        if top_n < 1:
            raise ValueError("top_n must be at least 1")

        # Limit top_n to available documents
        top_n = min(top_n, len(documents))

        logger.debug(
            f"Reranking {len(documents)} documents, returning top {top_n}",
            query_length=len(query)
        )

        # Score all query-document pairs
        pairs = [(query, doc) for doc in documents]
        scores = await self.score_pairs(pairs)

        # Create results with original indices
        results = [
            RerankResult(text=doc, score=score, index=idx)
            for idx, (doc, score) in enumerate(zip(documents, scores))
        ]

        # Sort by score (descending) and take top_n
        results.sort(key=lambda x: x.score, reverse=True)
        top_results = results[:top_n]

        logger.info(
            f"Reranked {len(documents)} documents to top {len(top_results)}",
            score_range=(
                f"{top_results[-1].score:.3f}-{top_results[0].score:.3f}"
                if top_results else "N/A"
            )
        )

        return top_results

    async def score_pairs(
        self,
        pairs: List[Tuple[str, str]]
    ) -> List[float]:
        """
        Score query-document pairs using FPT Cloud API

        Args:
            pairs: List of (query, document) tuples

        Returns:
            List of relevance scores (0-1) for each pair

        Raises:
            ValueError: If pairs list is empty
            RuntimeError: If API call fails
        """
        if not pairs:
            raise ValueError("Pairs list cannot be empty")

        logger.debug(f"Scoring {len(pairs)} query-document pairs")

        # Prepare API request
        # Note: Actual API format may differ - adjust based on FPT documentation
        url = f"{self._api_base}/rerank"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

        # Format request according to FPT API documentation
        # https://github.com/fpt-corp/ai-marketplace/blob/main/API%20Integration%20-%20Rerank%20model.md
        payload = {
            "model": self._model,
            "query": pairs[0][0],  # First query (assuming all same)
            "documents": [doc for _, doc in pairs],
            "top_n": len(pairs)  # Get scores for all
        }

        # Make API call with retries
        for attempt in range(self._max_retries):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(
                        url,
                        headers=headers,
                        json=payload
                    )
                    response.raise_for_status()

                    # Parse response
                    data = response.json()

                    # Extract scores
                    # Adjust based on actual API response format
                    if "results" in data:
                        scores = [
                            result.get("relevance_score", 0.0)
                            for result in data["results"]
                        ]
                    elif "scores" in data:
                        scores = data["scores"]
                    else:
                        # Fallback: assume direct score list
                        scores = data.get("data", [])

                    # Normalize scores to 0-1 if needed
                    scores = self._normalize_scores(scores)

                    logger.debug(
                        f"Scored {len(scores)} pairs successfully",
                        attempt=attempt + 1
                    )

                    return scores

            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error during reranking (attempt {attempt + 1})",
                    status_code=e.response.status_code,
                    response=e.response.text[:200]
                )

                if attempt == self._max_retries - 1:
                    raise RuntimeError(
                        f"Reranking failed after {self._max_retries} attempts: {e}"
                    )

                # Exponential backoff
                await asyncio.sleep(2 ** attempt)

            except Exception as e:
                logger.error(
                    f"Unexpected error during reranking (attempt {attempt + 1})",
                    error=str(e)
                )

                if attempt == self._max_retries - 1:
                    raise RuntimeError(f"Reranking failed: {e}")

                await asyncio.sleep(2 ** attempt)

        # Should not reach here
        raise RuntimeError("Reranking failed for unknown reason")

    def _normalize_scores(self, scores: List[float]) -> List[float]:
        """
        Normalize scores to 0-1 range

        Args:
            scores: Raw scores from API

        Returns:
            Normalized scores between 0 and 1
        """
        if not scores:
            return []

        # If already in 0-1 range, return as-is
        if all(0 <= s <= 1 for s in scores):
            return scores

        # Min-max normalization
        min_score = min(scores)
        max_score = max(scores)

        if max_score == min_score:
            # All same score
            return [0.5] * len(scores)

        normalized = [
            (score - min_score) / (max_score - min_score)
            for score in scores
        ]

        logger.debug(
            "Normalized scores",
            original_range=f"{min_score:.3f}-{max_score:.3f}",
            normalized_range="0.000-1.000"
        )

        return normalized

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the reranker model

        Returns:
            Dictionary with model details
        """
        return {
            "name": self._model,
            "provider": "FPT Cloud",
            "type": "reranker",
            "multilingual": True,
            "supports_vietnamese": True,
            "max_query_length": 512,
            "max_document_length": 512,
            "api_base": self._api_base
        }


# For backward compatibility
class BgeRerankerAdapter(FptRerankerAdapter):
    """Alias for FptRerankerAdapter"""
    pass
