"""
Semantic Similarity Module
Detects similar questions using TF-IDF and Cosine Similarity.
Much more accurate than character-based SequenceMatcher.
"""

import re
from collections import defaultdict

# Try to import sklearn for TF-IDF
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ sklearn not available. Using fallback similarity method.")

# Fallback: difflib SequenceMatcher
from difflib import SequenceMatcher


def normalize_question(question):
    """
    Normalize a question for comparison.

    Args:
        question (str): Raw question text

    Returns:
        str: Normalized question text
    """
    if not question:
        return ""

    # Convert to lowercase
    text = question.lower()

    # Remove question numbers (Q1, 1., etc.)
    text = re.sub(r'^[Qq]?\d+[\.\)\:]?\s*', '', text)

    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text.strip()


def calculate_tfidf_similarity(questions):
    """
    Calculate similarity matrix using TF-IDF and Cosine Similarity.

    This is much more accurate than character-based matching because:
    1. TF-IDF weights important words higher
    2. Cosine similarity measures angle between vectors (semantic similarity)
    3. Handles different word orders and synonyms better

    Args:
        questions (list): List of question strings

    Returns:
        numpy.ndarray: Similarity matrix where [i][j] is similarity between questions i and j
    """
    if not SKLEARN_AVAILABLE or len(questions) < 2:
        return None

    # Normalize questions
    normalized = [normalize_question(q) for q in questions]

    # Filter out empty questions
    valid_questions = [(i, q) for i, q in enumerate(normalized) if q.strip()]

    if len(valid_questions) < 2:
        return None

    indices, texts = zip(*valid_questions)

    try:
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            min_df=1,
            stop_words='english',
            ngram_range=(1, 2)  # Use unigrams and bigrams
        )

        # Fit and transform questions to TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Calculate cosine similarity between all pairs
        similarity_matrix = cosine_similarity(tfidf_matrix)

        return similarity_matrix, indices

    except Exception as e:
        print(f"TF-IDF calculation error: {e}")
        return None


def calculate_fallback_similarity(q1, q2):
    """
    Fallback similarity using SequenceMatcher.
    Used when sklearn is not available.

    Args:
        q1 (str): First question
        q2 (str): Second question

    Returns:
        float: Similarity ratio (0 to 1)
    """
    n1 = normalize_question(q1)
    n2 = normalize_question(q2)

    if not n1 or not n2:
        return 0.0

    return SequenceMatcher(None, n1, n2).ratio()


def group_similar_questions(questions, threshold=0.65):
    """
    Group similar questions together based on semantic similarity.

    This function:
    1. Calculates similarity between all question pairs
    2. Groups questions that exceed the similarity threshold
    3. Returns groups with representative questions

    Args:
        questions (list): List of question strings
        threshold (float): Similarity threshold (0.65 = 65% similar)

    Returns:
        list: List of question groups, each containing:
            - representative: The main question text
            - variants: List of similar question texts
            - count: Number of similar questions (frequency)
            - indices: Original indices of grouped questions
    """
    if not questions or len(questions) == 0:
        return []

    n = len(questions)

    # Track which questions have been assigned to a group
    assigned = [False] * n
    groups = []

    # Try TF-IDF similarity first
    tfidf_result = calculate_tfidf_similarity(questions)

    if tfidf_result is not None:
        similarity_matrix, valid_indices = tfidf_result
        index_map = {original: new for new, original in enumerate(valid_indices)}

        print(f"✅ Using TF-IDF + Cosine Similarity (threshold: {threshold})")

        for i in range(n):
            if assigned[i]:
                continue

            # Start a new group with this question
            group = {
                'representative': questions[i],
                'variants': [questions[i]],
                'count': 1,
                'indices': [i]
            }
            assigned[i] = True

            # Find similar questions
            if i in index_map:
                matrix_i = index_map[i]

                for j in range(i + 1, n):
                    if assigned[j]:
                        continue

                    if j in index_map:
                        matrix_j = index_map[j]
                        similarity = similarity_matrix[matrix_i][matrix_j]

                        if similarity >= threshold:
                            group['variants'].append(questions[j])
                            group['count'] += 1
                            group['indices'].append(j)
                            assigned[j] = True

            groups.append(group)

    else:
        # Fallback to SequenceMatcher
        print(f"⚠️ Using fallback SequenceMatcher (threshold: {threshold})")

        for i in range(n):
            if assigned[i]:
                continue

            group = {
                'representative': questions[i],
                'variants': [questions[i]],
                'count': 1,
                'indices': [i]
            }
            assigned[i] = True

            for j in range(i + 1, n):
                if assigned[j]:
                    continue

                similarity = calculate_fallback_similarity(questions[i], questions[j])

                if similarity >= threshold:
                    group['variants'].append(questions[j])
                    group['count'] += 1
                    group['indices'].append(j)
                    assigned[j] = True

            groups.append(group)

    # Sort groups by count (most repeated first)
    groups.sort(key=lambda x: x['count'], reverse=True)

    return groups


def find_repeated_questions(questions, min_occurrences=2, threshold=0.65):
    """
    Find questions that appear multiple times across papers.

    Args:
        questions (list): List of all extracted questions
        min_occurrences (int): Minimum times a question must appear
        threshold (float): Similarity threshold for grouping

    Returns:
        list: List of repeated question groups
    """
    groups = group_similar_questions(questions, threshold)

    # Filter to only repeated questions
    repeated = [g for g in groups if g['count'] >= min_occurrences]

    return repeated


def classify_importance(count, total_papers):
    """
    Classify question importance based on frequency.

    Args:
        count (int): Number of times question appeared
        total_papers (int): Total number of papers analyzed

    Returns:
        tuple: (importance_level, importance_label, color_code)
    """
    if total_papers == 0:
        total_papers = 1

    frequency_ratio = count / total_papers

    if count >= 4 or frequency_ratio >= 0.8:
        return (3, "Highly Important", "#ff4757")  # Red
    elif count >= 2 or frequency_ratio >= 0.4:
        return (2, "Important", "#ffa502")  # Orange
    else:
        return (1, "Moderately Important", "#2ed573")  # Green


# Testing
if __name__ == "__main__":
    print("=" * 60)
    print("SEMANTIC SIMILARITY MODULE - TEST")
    print("=" * 60)

    test_questions = [
        "Explain the OSI model in detail.",
        "Describe the OSI reference model architecture.",
        "What are the layers of OSI model?",
        "Define TCP/IP protocol.",
        "Explain TCP/IP protocol suite.",
        "What is machine learning?",
        "Define machine learning and its types.",
        "Explain neural networks.",
        "What are artificial neural networks?",
    ]

    print(f"\nGrouping {len(test_questions)} questions...\n")

    groups = group_similar_questions(test_questions, threshold=0.5)

    for i, group in enumerate(groups, 1):
        print(f"Group {i} (Count: {group['count']}):")
        print(f"  Representative: {group['representative']}")
        if group['count'] > 1:
            print(f"  Variants:")
            for v in group['variants'][1:]:
                print(f"    - {v}")
        print()

