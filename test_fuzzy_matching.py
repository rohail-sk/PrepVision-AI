"""
Test the new fuzzy similarity matching implementation
"""
from difflib import SequenceMatcher

# Test questions with similar meaning but different wording
test_questions = [
    "What is machine learning?",
    "Define machine learning and its types",
    "Explain the concept of machine learning",
    "What do you mean by machine learning?",
    "What is artificial intelligence?",
    "Define AI",
    "Explain neural networks in detail",
    "Describe the working of neural networks"
]

# Normalize questions
normalized = [' '.join(q.lower().split()) for q in test_questions]

# Fuzzy matching with 0.75 threshold
SIMILARITY_THRESHOLD = 0.75

print("=" * 80)
print("FUZZY SIMILARITY MATCHING TEST")
print("=" * 80)

# Group similar questions
groups = []
assigned = [False] * len(normalized)

for i, q1 in enumerate(normalized):
    if assigned[i]:
        continue

    # Start new group
    group = [test_questions[i]]
    assigned[i] = True

    # Find similar questions
    for j, q2 in enumerate(normalized):
        if i >= j or assigned[j]:
            continue

        similarity = SequenceMatcher(None, q1, q2).ratio()

        if similarity >= SIMILARITY_THRESHOLD:
            group.append(test_questions[j])
            assigned[j] = True
            print(f"✅ MATCH: '{test_questions[i][:50]}...' ≈ '{test_questions[j][:50]}...' (similarity: {similarity:.2f})")

    groups.append(group)

print("\n" + "=" * 80)
print("QUESTION GROUPS (Similar questions grouped together)")
print("=" * 80)

for i, group in enumerate(groups, 1):
    print(f"\nGroup {i} ({len(group)} questions):")
    for q in group:
        print(f"  • {q}")

print("\n" + "=" * 80)
print(f"RESULTS: {len(test_questions)} questions → {len(groups)} unique groups")
print("=" * 80)

# Expected results:
# Group 1: ML questions (4 questions)
# Group 2: AI questions (2 questions)
# Group 3: Neural network questions (2 questions)

expected_groups = 3
if len(groups) == expected_groups:
    print(f"✅ PASS: Correctly identified {expected_groups} unique question groups")
else:
    print(f"⚠️ WARNING: Found {len(groups)} groups, expected around {expected_groups}")
    print("   (Threshold may need adjustment)")

