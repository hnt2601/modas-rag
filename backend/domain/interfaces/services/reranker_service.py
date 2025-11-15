"""
Reranker Service Interface

This module defines the contract for reranking services.
Rerankers improve retrieval quality by re-scoring documents based on relevance.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class RerankResult:
    """Result from reranking operation"""

    text: str
    score: float
    index: int  # Original index in input list

    def __post_init__(self):
        """Validate rerank result"""
        if not isinstance(self.score, (int, float)):
            raise ValueError("Score must be numeric")
        if self.score < 0 or self.score > 1:
            raise ValueError("Score must be between 0 and 1")


class IRerankerService(ABC):
    """
    Contract for reranking services

    Rerankers take a query and a list of documents, then re-score them
    based on relevance to improve retrieval quality.

    Example Usage:
        query = "What is machine learning?"
        documents = [
            "Machine learning is a subset of AI...",
            "Python is a programming language...",
            "Deep learning uses neural networks..."
        ]

        results = await reranker.rerank(query, documents, top_n=2)
        # Returns top 2 most relevant documents with scores
    """

    @abstractmethod
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_n: int = 5
    ) -> List[RerankResult]:
        """
        Rerank documents based on relevance to query

        Args:
            query: The search query
            documents: List of document texts to rerank
            top_n: Number of top results to return

        Returns:
            List of RerankResult ordered by relevance (highest first)

        Raises:
            ValueError: If query is empty or documents list is empty
            RuntimeError: If reranking fails
        """
        pass

    @abstractmethod
    async def score_pairs(
        self,
        pairs: List[Tuple[str, str]]
    ) -> List[float]:
        """
        Score query-document pairs

        Args:
            pairs: List of (query, document) tuples

        Returns:
            List of relevance scores (0-1) for each pair

        Raises:
            ValueError: If pairs list is empty
            RuntimeError: If scoring fails
        """
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Get information about the reranker model

        Returns:
            Dictionary with model name, max_length, etc.
        """
        pass
