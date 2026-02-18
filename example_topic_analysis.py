"""
Example: Using Topic Analysis for Question Paper Analysis
This script demonstrates how to use the analyze_topics function
to identify important topics and rank questions by importance.
"""

from modules.preprocessing import preprocess_text, extract_questions, analyze_topics

# Sample question paper text
sample_question_paper = """
Q1. Define database management system and explain its advantages.
A database management system (DBMS) is software that allows users to create, 
manage, and manipulate databases efficiently.

Q2. What are the different types of database models?
Explain hierarchical, network, relational, and object-oriented database models.

Q3. Explain normalization in database design.
Normalization is the process of organizing database tables to reduce redundancy 
and improve data integrity.

Q4. What is SQL? Write queries for creating and managing database tables.
SQL (Structured Query Language) is used for managing relational databases.

Q5. Describe ACID properties in database transactions.
ACID stands for Atomicity, Consistency, Isolation, and Durability.

Q6. What is the difference between SQL and NoSQL databases?
SQL databases are relational while NoSQL databases use different data models.

Q7. Explain indexing and its importance in database performance.
Indexing improves query performance by creating efficient data access paths.

Q8. Define primary key, foreign key, and candidate key.
Keys are used to establish relationships and ensure data uniqueness in databases.
"""

print("="*70)
print("QUESTION PAPER TOPIC ANALYSIS DEMO")
print("="*70)

# Step 1: Preprocess the text
print("\n📝 Step 1: Preprocessing the question paper...")
cleaned_text, tokens = preprocess_text(sample_question_paper)
print(f"   ✓ Generated {len(tokens)} tokens")

# Step 2: Extract questions
print("\n📋 Step 2: Extracting questions...")
questions = extract_questions(sample_question_paper)
print(f"   ✓ Found {len(questions)} questions")

# Step 3: Analyze topics and rank questions
print("\n🔍 Step 3: Analyzing topics and ranking questions...")
analysis = analyze_topics(tokens, questions)

# Display results
print("\n" + "="*70)
print("📊 ANALYSIS RESULTS")
print("="*70)

print("\n🎯 KEY STATISTICS:")
print(f"   • Total Questions: {len(questions)}")
print(f"   • Unique Keywords: {analysis['keyword_count']}")
print(f"   • Average Importance Score: {analysis['avg_score']:.2f}")

print("\n🔥 TOP 10 KEYWORDS (Most Frequent Topics):")
print("-"*70)
for i, (word, frequency) in enumerate(analysis['top_keywords'], 1):
    bar = "█" * min(frequency, 20)  # Visual bar chart
    print(f"   {i:2d}. {word:15s} | {bar} ({frequency} occurrences)")

print("\n🏆 RANKED QUESTIONS (By Importance):")
print("-"*70)
for i, (question, score, original_idx) in enumerate(analysis['ranked_questions'], 1):
    # Create preview of question
    preview = question[:70].replace('\n', ' ').strip()
    if len(question) > 70:
        preview += "..."

    # Determine importance level
    if score >= analysis['avg_score'] * 1.5:
        importance = "🔴 HIGH"
    elif score >= analysis['avg_score']:
        importance = "🟡 MEDIUM"
    else:
        importance = "🟢 LOW"

    print(f"\n   {i}. {importance} | Score: {score:.2f}")
    print(f"      Original Q{original_idx}: {preview}")

print("\n" + "="*70)
print("💡 INSIGHTS:")
print("="*70)
print("   • Questions with higher scores contain more frequently mentioned topics")
print("   • These are likely to be more important or commonly asked questions")
print("   • Focus on high-scoring questions for exam preparation")

print("\n" + "="*70)
print("✅ ANALYSIS COMPLETE")
print("="*70)

# Additional: Show which keywords appear in top question
print("\n📌 DETAILED BREAKDOWN - Top Question Analysis:")
print("-"*70)
if analysis['ranked_questions']:
    top_question, top_score, top_idx = analysis['ranked_questions'][0]
    print(f"\n   Top Question (Q{top_idx}):")
    print(f"   {top_question[:150]}...")
    print(f"\n   Why it scored {top_score:.2f}:")

    # Find which keywords from top 10 appear in this question
    top_keywords_set = set([word for word, _ in analysis['top_keywords'][:10]])
    question_words = set(top_question.lower().split())

    matching_keywords = top_keywords_set.intersection(question_words)
    print(f"   • Contains {len(matching_keywords)} top keywords:")
    for keyword in sorted(matching_keywords):
        print(f"     - '{keyword}'")

print("\n" + "="*70)

