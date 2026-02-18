"""
Integration Test: Verify Topic Analysis Module
Tests that all functions can be imported and used correctly.
"""

print("="*70)
print("TOPIC ANALYSIS MODULE - INTEGRATION TEST")
print("="*70)

# Test 1: Import from modules package
print("\n[*] Test 1: Testing imports...")
try:
    from modules import preprocess_text, extract_questions, analyze_text, analyze_topics
    print("  [PASS] All functions imported successfully from 'modules' package")
except ImportError as e:
    print(f"  [FAIL] Import failed: {e}")
    # Define fallback to prevent undefined variable warnings
    preprocess_text = extract_questions = analyze_text = analyze_topics = None
    exit(1)

# Test 2: Import directly from preprocessing
print("\n[*] Test 2: Testing direct imports...")
try:
    from modules.preprocessing import analyze_topics as at
    print("  [PASS] Direct import successful")
except ImportError as e:
    print(f"  [FAIL] Direct import failed: {e}")
    exit(1)

# Test 3: Verify function exists and is callable
print("\n[*] Test 3: Verifying function signature...")
try:
    import inspect
    sig = inspect.signature(analyze_topics)
    params = list(sig.parameters.keys())
    assert params == ['tokens', 'questions'], f"Expected ['tokens', 'questions'], got {params}"
    print(f"  [PASS] Function signature correct: analyze_topics{sig}")
except Exception as e:
    print(f"  [FAIL] Signature verification failed: {e}")
    exit(1)

# Test 4: Run with sample data
print("\n[*] Test 4: Running with sample data...")
sample_text = """
Q1. What is machine learning?
Machine learning is a type of artificial intelligence.

Q2. Define neural networks.
Neural networks are inspired by the human brain.

Q3. Explain deep learning and its applications.
Deep learning uses multiple layers of neural networks.
"""

try:
    # Preprocess
    cleaned, tokens = preprocess_text(sample_text)
    print(f"  [PASS] Preprocessing successful: {len(tokens)} tokens")

    # Extract questions
    questions = extract_questions(sample_text)
    print(f"  [PASS] Question extraction successful: {len(questions)} questions")

    # Analyze topics
    result = analyze_topics(tokens, questions)
    print(f"  [PASS] Topic analysis successful")

except Exception as e:
    print(f"  [FAIL] Processing failed: {e}")
    exit(1)

# Test 5: Verify return structure
print("\n[*] Test 5: Verifying return structure...")
try:
    required_keys = ['top_keywords', 'ranked_questions', 'keyword_count', 'avg_score']
    for key in required_keys:
        assert key in result, f"Missing key: {key}"
    print(f"  [PASS] All required keys present: {required_keys}")

    # Verify data types
    assert isinstance(result['top_keywords'], list), "top_keywords should be a list"
    assert isinstance(result['ranked_questions'], list), "ranked_questions should be a list"
    assert isinstance(result['keyword_count'], int), "keyword_count should be an int"
    assert isinstance(result['avg_score'], (int, float)), "avg_score should be numeric"
    print(f"  [PASS] All data types correct")

except AssertionError as e:
    print(f"  [FAIL] Structure verification failed: {e}")
    exit(1)

# Test 6: Verify top_keywords format
print("\n[*] Test 6: Verifying top_keywords format...")
try:
    if len(result['top_keywords']) > 0:
        word, freq = result['top_keywords'][0]
        assert isinstance(word, str), "Keyword should be a string"
        assert isinstance(freq, int), "Frequency should be an int"
        print(f"  [PASS] Format correct: ('{word}', {freq})")
    else:
        print(f"  [WARN] No keywords found (acceptable if input is small)")
except Exception as e:
    print(f"  [FAIL] Format verification failed: {e}")
    exit(1)

# Test 7: Verify ranked_questions format
print("\n[*] Test 7: Verifying ranked_questions format...")
try:
    if len(result['ranked_questions']) > 0:
        question, score, idx = result['ranked_questions'][0]
        assert isinstance(question, str), "Question should be a string"
        assert isinstance(score, (int, float)), "Score should be numeric"
        assert isinstance(idx, int), "Index should be an int"
        print(f"  [PASS] Format correct: (question, {score:.2f}, {idx})")
    else:
        print(f"  [FAIL] No ranked questions found")
        exit(1)
except Exception as e:
    print(f"  [FAIL] Format verification failed: {e}")
    exit(1)

# Test 8: Verify ranking order (scores should be descending)
print("\n[*] Test 8: Verifying ranking order...")
try:
    scores = [score for _, score, _ in result['ranked_questions']]
    is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
    assert is_sorted, "Questions should be sorted by score (descending)"
    print(f"  [PASS] Questions properly ranked (scores: {[f'{s:.1f}' for s in scores[:3]]}...)")
except Exception as e:
    print(f"  [FAIL] Ranking verification failed: {e}")
    exit(1)

# Test 9: Edge case - empty inputs
print("\n[*] Test 9: Testing edge cases...")
try:
    empty_result = analyze_topics([], [])
    assert empty_result['top_keywords'] == [], "Should return empty list for empty input"
    assert empty_result['ranked_questions'] == [], "Should return empty list for empty input"
    print(f"  [PASS] Handles empty inputs correctly")
except Exception as e:
    print(f"  [FAIL] Edge case handling failed: {e}")
    exit(1)

# Test 10: Display sample results
print("\n[*] Test 10: Sample results display...")
print("\n  >> Top 5 Keywords:")
for i, (word, freq) in enumerate(result['top_keywords'][:5], 1):
    print(f"    {i}. {word}: {freq} times")

print("\n  >> Top 3 Ranked Questions:")
for i, (question, score, idx) in enumerate(result['ranked_questions'][:3], 1):
    preview = question[:50] + "..." if len(question) > 50 else question
    print(f"    {i}. [Score: {score:.2f}] {preview}")

print("\n  >> Statistics:")
print(f"    - Total Keywords: {result['keyword_count']}")
print(f"    - Average Score: {result['avg_score']:.2f}")

# All tests passed
print("\n" + "="*70)
print("ALL TESTS PASSED!")
print("="*70)
print("\nSummary:")
print("  [PASS] Imports working correctly")
print("  [PASS] Function signature correct")
print("  [PASS] Sample data processed successfully")
print("  [PASS] Return structure verified")
print("  [PASS] Data formats correct")
print("  [PASS] Ranking order verified")
print("  [PASS] Edge cases handled")
print("\n>> Topic Analysis Module is ready for production!")
print("="*70)




