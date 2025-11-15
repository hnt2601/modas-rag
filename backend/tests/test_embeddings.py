"""
Test script for Vietnamese Embedding service.

This script tests the embedding functionality without requiring Qdrant.
"""

import asyncio
from loguru import logger
from core.embeddings import (
    get_embeddings,
    embed_query,
    embed_documents,
    get_text_splitter,
)


async def test_embedding_service():
    """Test Vietnamese Embedding service."""
    
    print("\n" + "="*70)
    print("🧪 Testing Vietnamese Embedding Service")
    print("="*70 + "\n")
    
    # Test 1: Initialize embeddings model
    print("📝 Test 1: Initialize Embeddings Model")
    try:
        embeddings = get_embeddings()
        print(f"✅ Embeddings model initialized")
        print(f"   Model: Vietnamese_Embedding")
        print(f"   Dimensions: 1024\n")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}\n")
        return
    
    # Test 2: Embed a single query
    print("📝 Test 2: Embed Single Query (Vietnamese)")
    try:
        query = "Hệ thống RAG là gì?"
        vector = await embed_query(query)
        print(f"✅ Query embedded successfully")
        print(f"   Query: '{query}'")
        print(f"   Vector dimensions: {len(vector)}")
        print(f"   First 5 values: {vector[:5]}\n")
    except Exception as e:
        print(f"❌ Failed to embed query: {e}\n")
        return
    
    # Test 3: Embed multiple documents
    print("📝 Test 3: Embed Multiple Documents")
    try:
        texts = [
            "Xin chào, tôi là trợ lý AI.",
            "RAG là viết tắt của Retrieval-Augmented Generation.",
            "Hệ thống sử dụng vector database để tìm kiếm.",
        ]
        vectors = await embed_documents(texts)
        print(f"✅ Documents embedded successfully")
        print(f"   Number of documents: {len(texts)}")
        print(f"   Number of vectors: {len(vectors)}")
        print(f"   Vector dimensions: {len(vectors[0])}")
        print(f"   First doc preview: '{texts[0][:50]}...'\n")
    except Exception as e:
        print(f"❌ Failed to embed documents: {e}\n")
        return
    
    # Test 4: Test text splitter
    print("📝 Test 4: Text Chunking")
    try:
        splitter = get_text_splitter()
        long_text = """
        Hệ thống RAG (Retrieval-Augmented Generation) là một kiến trúc AI tiên tiến
        kết hợp khả năng tìm kiếm thông tin với khả năng sinh văn bản của các mô hình
        ngôn ngữ lớn. Hệ thống này hoạt động bằng cách đầu tiên tìm kiếm các tài liệu
        liên quan từ cơ sở dữ liệu vector, sau đó sử dụng thông tin này làm ngữ cảnh
        để sinh ra câu trả lời chính xác hơn.
        
        Vector database đóng vai trò quan trọng trong hệ thống RAG. Nó lưu trữ các
        embedding của tài liệu, cho phép tìm kiếm ngữ nghĩa nhanh chóng và chính xác.
        Qdrant là một trong những vector database phổ biến nhất hiện nay.
        """ * 3  # Repeat to make it longer
        
        chunks = splitter.split_text(long_text)
        print(f"✅ Text chunking successful")
        print(f"   Original length: {len(long_text)} characters")
        print(f"   Number of chunks: {len(chunks)}")
        print(f"   Avg chunk size: {sum(len(c) for c in chunks) // len(chunks)} characters")
        print(f"   First chunk preview: '{chunks[0][:80]}...'\n")
    except Exception as e:
        print(f"❌ Failed to chunk text: {e}\n")
        return
    
    # Test 5: Empty input handling
    print("📝 Test 5: Error Handling (Empty Input)")
    try:
        await embed_query("")
        print(f"❌ Should have raised ValueError\n")
    except ValueError as e:
        print(f"✅ Correctly handled empty input")
        print(f"   Error message: {e}\n")
    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")
    
    print("="*70)
    print("🎉 All tests completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_embedding_service())

