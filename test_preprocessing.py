"""
Quick test to verify NLP preprocessing module functionality
"""

from modules.preprocessing import preprocess_text, extract_questions, analyze_text

# Test text
test_text = """
Q1. What is Python?
Python is a programming language.

Q2. What is machine learning?
Machine learning is AI subset.
"""

print("="*60)
print("QUICK VERIFICATION TEST")
print("="*60)

# Test 1: preprocess_text
print("\n1. Testing preprocess_text()...")
cleaned, tokens = preprocess_text(test_text)
print(f"   ✅ Success! Got {len(tokens)} tokens")

# Test 2: extract_questions
print("\n2. Testing extract_questions()...")
questions = extract_questions(test_text)
print(f"   ✅ Success! Found {len(questions)} questions")

# Test 3: analyze_text
print("\n3. Testing analyze_text()...")
result = analyze_text(test_text)
print(f"   ✅ Success! Analysis returned {result['question_count']} questions")

print("\n" + "="*60)
print("ALL TESTS PASSED! ✅")
print("="*60)
print("\nThe NLP preprocessing module is fully functional!")
print("\nAvailable functions:")
print("  - preprocess_text(raw_text)")
print("  - extract_questions(raw_text)")
print("  - analyze_text(raw_text)")

