"""
Vietnamese Embedding service integration with FPT Cloud.

This module provides text embedding and document processing capabilities
using the Vietnamese_Embedding model from FPT Cloud Marketplace.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from core.config import settings


# ============================================================================
# Embedding Model Functions
# ============================================================================

def get_embeddings() -> OpenAIEmbeddings:
    """
    Get Vietnamese Embedding model from FPT Cloud.
    
    Returns an OpenAIEmbeddings instance configured for FPT Cloud's
    Vietnamese_Embedding model (1024 dimensions).
    
    Returns:
        OpenAIEmbeddings: Configured embedding model
        
    Example:
        >>> embeddings = get_embeddings()
        >>> vector = embeddings.embed_query("Xin chào")
        >>> len(vector)
        1024
    """
    try:
        embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.fpt_api_key,
            openai_api_base=settings.fpt_api_base,
            dimensions=settings.embedding_dimensions,
        )
        logger.info(
            f"Initialized embedding model: {settings.embedding_model} "
            f"({settings.embedding_dimensions} dimensions)"
        )
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {e}", exc_info=True)
        raise


async def embed_documents(texts: List[str]) -> List[List[float]]:
    """
    Embed multiple documents using Vietnamese Embedding model.
    
    This function is optimized for batch processing of multiple documents.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embedding vectors (each is a list of floats)
        
    Raises:
        Exception: If embedding generation fails
        
    Example:
        >>> texts = ["Xin chào", "Tạm biệt"]
        >>> embeddings = await embed_documents(texts)
        >>> len(embeddings)
        2
        >>> len(embeddings[0])
        1024
    """
    if not texts:
        logger.warning("Empty text list provided to embed_documents")
        return []
    
    try:
        embeddings_model = get_embeddings()
        logger.info(f"Embedding {len(texts)} documents...")
        
        # Use aembed_documents for async processing
        vectors = await embeddings_model.aembed_documents(texts)
        
        logger.info(
            f"Successfully embedded {len(texts)} documents "
            f"({len(vectors[0])} dimensions each)"
        )
        return vectors
        
    except Exception as e:
        logger.error(f"Failed to embed documents: {e}", exc_info=True)
        raise


async def embed_query(text: str) -> List[float]:
    """
    Embed a single query using Vietnamese Embedding model.
    
    This function is optimized for single query embedding.
    
    Args:
        text: Query text to embed
        
    Returns:
        Embedding vector as list of floats
        
    Raises:
        Exception: If embedding generation fails
        
    Example:
        >>> query = "Hệ thống RAG là gì?"
        >>> vector = await embed_query(query)
        >>> len(vector)
        1024
    """
    if not text or not text.strip():
        logger.warning("Empty query provided to embed_query")
        raise ValueError("Query text cannot be empty")
    
    try:
        embeddings_model = get_embeddings()
        logger.debug(f"Embedding query: {text[:50]}...")
        
        # Use aembed_query for async processing
        vector = await embeddings_model.aembed_query(text)
        
        logger.debug(f"Successfully embedded query ({len(vector)} dimensions)")
        return vector
        
    except Exception as e:
        logger.error(f"Failed to embed query: {e}", exc_info=True)
        raise


# ============================================================================
# Document Loading Functions
# ============================================================================

def load_document(file_path: str) -> List[Document]:
    """
    Load document based on file type.
    
    Supports: PDF (.pdf), Text (.txt), Word (.doc, .docx), Markdown (.md)
    
    Args:
        file_path: Path to the document file
        
    Returns:
        List of LangChain Document objects
        
    Raises:
        ValueError: If file type is not supported
        FileNotFoundError: If file doesn't exist
        
    Example:
        >>> docs = load_document("document.pdf")
        >>> len(docs)
        5
        >>> docs[0].page_content[:100]
        'This is the first page...'
    """
    path = Path(file_path)
    
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = path.suffix.lower()
    logger.info(f"Loading document: {path.name} (type: {file_ext})")
    
    try:
        if file_ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_ext == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        elif file_ext in ['.doc', '.docx']:
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_ext == '.md':
            loader = UnstructuredMarkdownLoader(file_path)
        else:
            logger.error(f"Unsupported file type: {file_ext}")
            raise ValueError(
                f"Unsupported file type: {file_ext}. "
                f"Supported types: .pdf, .txt, .doc, .docx, .md"
            )
        
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages/sections from {path.name}")
        return documents
        
    except Exception as e:
        logger.error(f"Failed to load document {file_path}: {e}", exc_info=True)
        raise


# ============================================================================
# Text Chunking Functions
# ============================================================================

def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Get configured text splitter for chunking documents.
    
    Uses RecursiveCharacterTextSplitter with settings from config:
    - chunk_size: Maximum chunk size in characters
    - chunk_overlap: Overlap between chunks to preserve context
    
    Returns:
        RecursiveCharacterTextSplitter: Configured text splitter
        
    Example:
        >>> splitter = get_text_splitter()
        >>> text = "Long document text..."
        >>> chunks = splitter.split_text(text)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
        is_separator_regex=False,
    )
    
    logger.debug(
        f"Text splitter configured: "
        f"chunk_size={settings.chunk_size}, "
        f"chunk_overlap={settings.chunk_overlap}"
    )
    
    return splitter


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks.
    
    Args:
        documents: List of LangChain Document objects
        
    Returns:
        List of chunked Document objects with preserved metadata
        
    Example:
        >>> docs = load_document("large_file.pdf")
        >>> chunks = split_documents(docs)
        >>> len(chunks) > len(docs)  # More chunks than original pages
        True
    """
    if not documents:
        logger.warning("Empty document list provided to split_documents")
        return []
    
    try:
        splitter = get_text_splitter()
        
        logger.info(f"Splitting {len(documents)} documents into chunks...")
        chunks = splitter.split_documents(documents)
        
        logger.info(
            f"Split into {len(chunks)} chunks "
            f"(avg {sum(len(c.page_content) for c in chunks) // len(chunks)} chars/chunk)"
        )
        
        return chunks
        
    except Exception as e:
        logger.error(f"Failed to split documents: {e}", exc_info=True)
        raise


# ============================================================================
# Complete Document Processing Pipeline
# ============================================================================

async def process_document(
    file_path: str,
    add_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Complete document processing pipeline.
    
    This function:
    1. Loads the document based on file type
    2. Splits into chunks
    3. Generates embeddings for each chunk
    4. Returns processed data ready for vector database
    
    Args:
        file_path: Path to the document file
        add_metadata: Optional additional metadata to add to each chunk
        
    Returns:
        Dictionary containing:
            - texts: List of chunk texts
            - embeddings: List of embedding vectors
            - metadata: List of metadata dicts for each chunk
            - stats: Processing statistics
            
    Raises:
        Exception: If any step in the pipeline fails
        
    Example:
        >>> result = await process_document("document.pdf")
        >>> result['stats']
        {
            'filename': 'document.pdf',
            'file_size': 1024000,
            'pages': 10,
            'chunks': 25,
            'avg_chunk_size': 900
        }
    """
    path = Path(file_path)
    
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    logger.info(f"Processing document: {path.name}")
    
    try:
        # Step 1: Load document
        documents = load_document(file_path)
        
        # Step 2: Split into chunks
        chunks = split_documents(documents)
        
        if not chunks:
            logger.warning(f"No chunks created from {path.name}")
            return {
                'texts': [],
                'embeddings': [],
                'metadata': [],
                'stats': {
                    'filename': path.name,
                    'file_size': path.stat().st_size,
                    'pages': len(documents),
                    'chunks': 0,
                    'error': 'No content extracted'
                }
            }
        
        # Step 3: Extract texts and prepare metadata
        texts = [chunk.page_content for chunk in chunks]
        
        metadata_list = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = {
                'source': str(path),
                'filename': path.name,
                'file_type': path.suffix.lower(),
                'file_size': path.stat().st_size,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'chunk_size': len(chunk.page_content),
            }
            
            # Add original document metadata
            if chunk.metadata:
                chunk_metadata.update(chunk.metadata)
            
            # Add custom metadata if provided
            if add_metadata:
                chunk_metadata.update(add_metadata)
            
            metadata_list.append(chunk_metadata)
        
        # Step 4: Generate embeddings
        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = await embed_documents(texts)
        
        # Calculate statistics
        stats = {
            'filename': path.name,
            'file_type': path.suffix.lower(),
            'file_size': path.stat().st_size,
            'pages': len(documents),
            'chunks': len(chunks),
            'avg_chunk_size': sum(len(t) for t in texts) // len(texts),
            'embedding_dimensions': len(embeddings[0]) if embeddings else 0,
        }
        
        logger.info(
            f"Successfully processed {path.name}: "
            f"{stats['chunks']} chunks, "
            f"{stats['embedding_dimensions']} dimensions"
        )
        
        return {
            'texts': texts,
            'embeddings': embeddings,
            'metadata': metadata_list,
            'stats': stats,
        }
        
    except Exception as e:
        logger.error(
            f"Failed to process document {path.name}: {e}",
            exc_info=True
        )
        raise


# ============================================================================
# Utility Functions
# ============================================================================

def validate_file(file_path: str, max_size: Optional[int] = None) -> bool:
    """
    Validate file before processing.
    
    Checks:
    - File exists
    - File is readable
    - File size within limits
    - File type is supported
    
    Args:
        file_path: Path to the file
        max_size: Maximum file size in bytes (default from settings)
        
    Returns:
        True if file is valid
        
    Raises:
        ValueError: If file is invalid
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Check file size
    max_size = max_size or settings.max_upload_size
    file_size = path.stat().st_size
    
    if file_size > max_size:
        raise ValueError(
            f"File too large: {file_size} bytes "
            f"(max: {max_size} bytes)"
        )
    
    # Check file type
    supported_extensions = ['.pdf', '.txt', '.doc', '.docx', '.md']
    if path.suffix.lower() not in supported_extensions:
        raise ValueError(
            f"Unsupported file type: {path.suffix}. "
            f"Supported: {', '.join(supported_extensions)}"
        )
    
    logger.debug(f"File validation passed: {path.name}")
    return True


def get_supported_file_types() -> List[str]:
    """
    Get list of supported file types.
    
    Returns:
        List of supported file extensions
    """
    return ['.pdf', '.txt', '.doc', '.docx', '.md']

