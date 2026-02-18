"""
PRACTICAL EXAMPLES - NLP Preprocessing Module Integration
Demonstrates how to use the preprocessing module in real scenarios
"""

from modules.preprocessing import preprocess_text, extract_questions, analyze_text

print("="*70)
print("NLP PREPROCESSING MODULE - PRACTICAL EXAMPLES")
print("="*70)

# ============================================================================
# EXAMPLE 1: Processing a Simple Question Paper
# ============================================================================
print("\n\n" + "="*70)
print("EXAMPLE 1: Processing a Simple Question Paper")
print("="*70)

question_paper_1 = """
Q1. What is Python and why is it popular?
Q2. Explain the difference between list and tuple.
Q3. What are decorators in Python?
"""

print("\nInput Text:")
print(question_paper_1)

# Extract questions
questions = extract_questions(question_paper_1)
print(f"\n✅ Extracted {len(questions)} questions:")
for i, q in enumerate(questions, 1):
    print(f"   {i}. {q}")

# Preprocess text
cleaned, tokens = preprocess_text(question_paper_1)
print(f"\n✅ Preprocessing Results:")
print(f"   - Total tokens: {len(tokens)}")
print(f"   - Sample tokens: {tokens[:10]}")

# ============================================================================
# EXAMPLE 2: Processing Multiple Question Formats
# ============================================================================
print("\n\n" + "="*70)
print("EXAMPLE 2: Mixed Question Formats")
print("="*70)

question_paper_2 = """
Q1. Define machine learning.

Q2) What is supervised learning?

1. Explain neural networks.

2. What is deep learning?
"""

print("\nInput Text:")
print(question_paper_2)

result = analyze_text(question_paper_2)
print(f"\n✅ Analysis Results:")
print(f"   - Questions found: {result['question_count']}")
print(f"   - Tokens extracted: {len(result['tokens'])}")
print(f"\n   Questions:")
for i, q in enumerate(result['questions'], 1):
    print(f"   {i}. {q.strip()}")

# ============================================================================
# EXAMPLE 3: Processing Real OCR Text (with errors)
# ============================================================================
print("\n\n" + "="*70)
print("EXAMPLE 3: Processing OCR Text with Errors")
print("="*70)

ocr_text = """
Q1. Wh@t is Artif1cial Intell1gence?
AI is the simu1ation of human intelligence by machines.

Q2. Explain Machine Le@rning concepts?
ML is a subset of AI th@t enables computers to learn.
"""

print("\nOCR Input (with errors):")
print(ocr_text)

# Preprocessing will clean up special characters and numbers
cleaned, tokens = preprocess_text(ocr_text)
print(f"\n✅ After Preprocessing:")
print(f"   - Cleaned text: {cleaned[:100]}...")
print(f"   - Key tokens: {tokens[:15]}")

questions = extract_questions(ocr_text)
print(f"\n✅ Extracted Questions:")
for i, q in enumerate(questions, 1):
    print(f"   {i}. {q}")

# ============================================================================
# EXAMPLE 4: Integration with File Processing
# ============================================================================
print("\n\n" + "="*70)
print("EXAMPLE 4: Simulated File Processing Workflow")
print("="*70)

def process_uploaded_file(file_content):
    """
    Simulates processing an uploaded file's text content
    """
    print("\n📄 Processing uploaded file...")

    # Step 1: Extract questions
    questions = extract_questions(file_content)
    print(f"   ✅ Step 1: Extracted {len(questions)} questions")

    # Step 2: Preprocess text
    cleaned, tokens = preprocess_text(file_content)
    print(f"   ✅ Step 2: Generated {len(tokens)} tokens")

    # Step 3: Analyze
    result = analyze_text(file_content)
    print(f"   ✅ Step 3: Complete analysis done")

    return result

# Simulate file content
sample_file_content = """
Q1. What is Flask?
Q2. Explain REST API.
Q3. What is JSON?
"""

print("\nSimulated File Content:")
print(sample_file_content)

result = process_uploaded_file(sample_file_content)
print(f"\n📊 Final Results:")
print(f"   - Total Questions: {result['question_count']}")
print(f"   - Total Tokens: {len(result['tokens'])}")

# ============================================================================
# EXAMPLE 5: Token Analysis for Keyword Extraction
# ============================================================================
print("\n\n" + "="*70)
print("EXAMPLE 5: Keyword Extraction from Question Paper")
print("="*70)

question_paper_3 = """
Q1. Explain database normalization and its types.
Q2. What is the difference between SQL and NoSQL databases?
Q3. Define ACID properties in database systems.
Q4. What are database indexes and their importance?
"""

print("\nInput Text:")
print(question_paper_3)

# Preprocess to get tokens
cleaned, tokens = preprocess_text(question_paper_3)

# Count token frequency
from collections import Counter
token_freq = Counter(tokens)
top_keywords = token_freq.most_common(10)

print(f"\n✅ Top 10 Keywords (by frequency):")
for word, count in top_keywords:
    print(f"   - '{word}': {count} times")

# ============================================================================
# EXAMPLE 6: Batch Processing Multiple Papers
# ============================================================================
print("\n\n" + "="*70)
print("EXAMPLE 6: Batch Processing Multiple Question Papers")
print("="*70)

papers = [
    "Q1. What is Python?\nQ2. What is Java?",
    "1. Define AI.\n2. Define ML.",
    "Q1) What is React?\nQ2) What is Node.js?"
]

print(f"\n📚 Processing {len(papers)} question papers...\n")

all_results = []
for i, paper in enumerate(papers, 1):
    result = analyze_text(paper)
    all_results.append(result)
    print(f"   Paper {i}: {result['question_count']} questions, {len(result['tokens'])} tokens")

total_questions = sum(r['question_count'] for r in all_results)
total_tokens = sum(len(r['tokens']) for r in all_results)

print(f"\n✅ Batch Results:")
print(f"   - Total Papers Processed: {len(papers)}")
print(f"   - Total Questions Extracted: {total_questions}")
print(f"   - Total Tokens Generated: {total_tokens}")

# ============================================================================
print("\n\n" + "="*70)
print("ALL EXAMPLES COMPLETED SUCCESSFULLY! ✅")
print("="*70)
print("\n💡 Key Takeaways:")
print("   1. Module handles various question formats (Q1., 1., Q1))")
print("   2. Preprocessing cleans and normalizes text effectively")
print("   3. Can process OCR text with errors")
print("   4. Easy integration with file upload workflows")
print("   5. Supports keyword extraction and analysis")
print("   6. Batch processing capability for multiple papers")
print("\n���� Ready for production use in PrepVision AI!")
print("="*70)

