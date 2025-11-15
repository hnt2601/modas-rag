"""
Test script for BGE Reranker v2-m3

This script tests the reranker functionality with sample data.
Run this to verify the reranker is working correctly.

Usage:
    python test_reranker.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from infrastructure.ai.reranking import RerankerFactory
from core.config import Settings
from loguru import logger


async def test_basic_reranking():
    """Test basic reranking functionality"""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Reranking")
    print("=" * 60)

    # Initialize reranker
    settings = Settings()
    reranker = RerankerFactory.create(settings)

    # Sample query and documents
    query = "What is machine learning?"

    documents = [
        "Python is a high-level programming language known for its simplicity.",
        "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
        "The weather today is sunny with a chance of rain in the afternoon.",
        "Deep learning uses neural networks with multiple layers to learn complex patterns.",
        "JavaScript is commonly used for web development and creating interactive websites."
    ]

    print(f"\nQuery: {query}")
    print(f"Documents to rerank: {len(documents)}")
    print("\nOriginal documents:")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc[:60]}...")

    # Rerank
    try:
        results = await reranker.rerank(
            query=query,
            documents=documents,
            top_n=3
        )

        print(f"\n✅ Reranking successful!")
        print(f"Top {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. Score: {result.score:.4f} (Original index: {result.index})")
            print(f"     {result.text[:80]}...")

        # Verify most relevant documents are top-ranked
        assert results[0].score > results[1].score, "Scores should be descending"
        assert "machine learning" in results[0].text.lower(), "Most relevant doc should mention ML"

        print("\n✅ Test passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.error("Reranking test failed", error=str(e))
        return False


async def test_vietnamese_reranking():
    """Test reranking with Vietnamese text"""
    print("\n" + "=" * 60)
    print("TEST 2: Vietnamese Text Reranking")
    print("=" * 60)

    settings = Settings()
    reranker = RerankerFactory.create(settings)

    query = "Trí tuệ nhân tạo là gì?"

    documents = [
        "Python là ngôn ngữ lập trình bậc cao được ưa chuộng trong phát triển phần mềm.",
        "Trí tuệ nhân tạo (AI) là khả năng của máy tính để thực hiện các tác vụ thông minh.",
        "Thời tiết hôm nay nắng đẹp, nhiệt độ khoảng 28 độ C.",
        "Machine learning là một nhánh của AI giúp máy tính học từ dữ liệu.",
        "React là thư viện JavaScript phổ biến để xây dựng giao diện người dùng."
    ]

    print(f"\nQuery: {query}")
    print(f"Documents: {len(documents)}")

    try:
        results = await reranker.rerank(
            query=query,
            documents=documents,
            top_n=3
        )

        print(f"\n✅ Vietnamese reranking successful!")
        print(f"Top {len(results)} kết quả:")
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. Điểm: {result.score:.4f}")
            print(f"     {result.text[:80]}...")

        print("\n✅ Test passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.error("Vietnamese reranking test failed", error=str(e))
        return False


async def test_score_pairs():
    """Test scoring query-document pairs"""
    print("\n" + "=" * 60)
    print("TEST 3: Score Pairs")
    print("=" * 60)

    settings = Settings()
    reranker = RerankerFactory.create(settings)

    pairs = [
        ("What is AI?", "Artificial intelligence is the simulation of human intelligence."),
        ("What is AI?", "Python is a programming language."),
        ("What is AI?", "Machine learning is a subset of AI."),
    ]

    print(f"\nScoring {len(pairs)} query-document pairs...")

    try:
        scores = await reranker.score_pairs(pairs)

        print(f"\n✅ Scoring successful!")
        for i, ((query, doc), score) in enumerate(zip(pairs, scores), 1):
            print(f"\n  Pair {i}:")
            print(f"    Query: {query}")
            print(f"    Doc: {doc[:60]}...")
            print(f"    Score: {score:.4f}")

        # Verify scores are normalized
        assert all(0 <= s <= 1 for s in scores), "Scores should be normalized to 0-1"

        print("\n✅ Test passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.error("Score pairs test failed", error=str(e))
        return False


async def test_model_info():
    """Test getting model information"""
    print("\n" + "=" * 60)
    print("TEST 4: Model Information")
    print("=" * 60)

    settings = Settings()
    reranker = RerankerFactory.create(settings)

    info = reranker.get_model_info()

    print("\n✅ Model Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    assert info["name"] == settings.reranker_model
    assert info["type"] == "reranker"

    print("\n✅ Test passed!")
    return True


async def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "=" * 60)
    print("TEST 5: Edge Cases & Error Handling")
    print("=" * 60)

    settings = Settings()
    reranker = RerankerFactory.create(settings)

    # Test 1: Empty query
    print("\n  Test 5.1: Empty query...")
    try:
        await reranker.rerank("", ["doc1", "doc2"])
        print("  ❌ Should have raised ValueError")
        return False
    except ValueError as e:
        print(f"  ✅ Correctly raised ValueError: {e}")

    # Test 2: Empty documents
    print("\n  Test 5.2: Empty documents...")
    try:
        await reranker.rerank("query", [])
        print("  ❌ Should have raised ValueError")
        return False
    except ValueError as e:
        print(f"  ✅ Correctly raised ValueError: {e}")

    # Test 3: top_n larger than documents
    print("\n  Test 5.3: top_n > len(documents)...")
    try:
        results = await reranker.rerank(
            "query",
            ["doc1", "doc2"],
            top_n=10
        )
        assert len(results) == 2, "Should return only available documents"
        print(f"  ✅ Correctly returned {len(results)} results (not 10)")
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False

    print("\n✅ All edge case tests passed!")
    return True


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("BGE Reranker v2-m3 Test Suite")
    print("=" * 60)

    # Check if API key is configured
    settings = Settings()
    if settings.fpt_api_key == "your-fpt-api-key-here":
        print("\n⚠️  WARNING: FPT API key not configured!")
        print("   Please set FPT_API_KEY in .env file")
        print("   Some tests may fail without a valid API key")
        print()

    # Run tests
    tests = [
        ("Basic Reranking", test_basic_reranking),
        ("Vietnamese Reranking", test_vietnamese_reranking),
        ("Score Pairs", test_score_pairs),
        ("Model Info", test_model_info),
        ("Edge Cases", test_edge_cases),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"Test '{name}' crashed", error=str(e))
            results.append((name, False))
            print(f"\n❌ Test '{name}' crashed: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")

    print(f"\n  Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
