"""
Question Ranker Module
Ranks questions by importance based on multiple factors.
"""

from collections import Counter


def calculate_importance_score(question, frequency, topic_score, keyword_matches, total_papers):
    """
    Calculate comprehensive importance score for a question.

    Scoring factors:
    1. Frequency (40%) - How often the question appears
    2. Topic relevance (30%) - How central the topic is
    3. Keyword density (20%) - Important keywords in question
    4. Length factor (10%) - Longer questions often more important

    Args:
        question (str): Question text
        frequency (int): Number of times question appeared
        topic_score (float): Topic relevance score
        keyword_matches (int): Number of top keywords matched
        total_papers (int): Total papers analyzed

    Returns:
        float: Importance score (0-100)
    """
    # Frequency score (0-40)
    # Normalize by total papers
    freq_ratio = frequency / max(total_papers, 1)
    freq_score = min(freq_ratio * 40, 40)

    # Topic score (0-30)
    topic_normalized = min(topic_score * 10, 30)

    # Keyword score (0-20)
    keyword_score = min(keyword_matches * 4, 20)

    # Length score (0-10)
    # Questions between 50-200 chars are ideal
    length = len(question)
    if 50 <= length <= 200:
        length_score = 10
    elif length > 200:
        length_score = 8
    elif length >= 30:
        length_score = 6
    else:
        length_score = 3

    total_score = freq_score + topic_normalized + keyword_score + length_score

    return round(total_score, 2)


def classify_importance_level(score, frequency):
    """
    Classify question importance based on score and frequency.

    Args:
        score (float): Importance score
        frequency (int): Appearance frequency

    Returns:
        dict: Classification with level, label, and color
    """
    if frequency >= 4 or score >= 70:
        return {
            'level': 3,
            'label': 'Highly Important',
            'color': '#ff4757',
            'badge': '🔴'
        }
    elif frequency >= 2 or score >= 40:
        return {
            'level': 2,
            'label': 'Important',
            'color': '#ffa502',
            'badge': '🟠'
        }
    else:
        return {
            'level': 1,
            'label': 'Moderately Important',
            'color': '#2ed573',
            'badge': '🟢'
        }


def rank_questions(question_groups, topic_analysis, total_papers):
    """
    Rank all questions by importance.

    Args:
        question_groups (list): Grouped similar questions from similarity module
        topic_analysis (dict): Results from topic analysis module
        total_papers (int): Number of papers analyzed

    Returns:
        list: Ranked questions with scores and classifications
    """
    print("\n" + "=" * 50)
    print("📊 QUESTION RANKING")
    print("=" * 50)

    # Get top keywords for scoring
    top_keywords = set(kw for kw, count in topic_analysis.get('top_keywords', []))

    ranked_questions = []

    for group in question_groups:
        question = group['representative']
        frequency = group['count']

        # Find topic score from analysis
        topic_score = 0
        for qa in topic_analysis.get('question_analysis', []):
            if qa['question'] == question:
                topic_score = qa.get('topic_score', 0)
                break

        # Count keyword matches
        question_lower = question.lower()
        keyword_matches = sum(1 for kw in top_keywords if kw in question_lower)

        # Calculate importance score
        importance_score = calculate_importance_score(
            question, frequency, topic_score, keyword_matches, total_papers
        )

        # Classify importance
        classification = classify_importance_level(importance_score, frequency)

        ranked_questions.append({
            'question': question,
            'frequency': frequency,
            'variants': group.get('variants', [question]),
            'importance_score': importance_score,
            'classification': classification,
            'topic_score': topic_score,
            'keyword_matches': keyword_matches
        })

    # Sort by importance score (highest first)
    ranked_questions.sort(key=lambda x: x['importance_score'], reverse=True)

    # Add rank numbers
    for i, q in enumerate(ranked_questions, 1):
        q['rank'] = i

    print(f"\n✅ Ranked {len(ranked_questions)} unique questions")
    print(f"   Highly Important: {sum(1 for q in ranked_questions if q['classification']['level'] == 3)}")
    print(f"   Important: {sum(1 for q in ranked_questions if q['classification']['level'] == 2)}")
    print(f"   Moderate: {sum(1 for q in ranked_questions if q['classification']['level'] == 1)}")

    return ranked_questions


def get_important_questions_report(ranked_questions, top_n=20):
    """
    Generate an important questions report.

    Args:
        ranked_questions (list): Ranked questions from rank_questions()
        top_n (int): Number of top questions to include

    Returns:
        dict: Report data for display/PDF generation
    """
    # Get top N questions
    top_questions = ranked_questions[:top_n]

    # Group by importance level
    highly_important = [q for q in top_questions if q['classification']['level'] == 3]
    important = [q for q in top_questions if q['classification']['level'] == 2]
    moderate = [q for q in top_questions if q['classification']['level'] == 1]

    report = {
        'title': 'Important Questions Report',
        'total_analyzed': len(ranked_questions),
        'top_count': len(top_questions),
        'sections': [
            {
                'name': 'Highly Important Questions',
                'description': 'Questions that appeared 4+ times or scored very high',
                'badge': '🔴',
                'color': '#ff4757',
                'questions': highly_important
            },
            {
                'name': 'Important Questions',
                'description': 'Questions that appeared 2-3 times',
                'badge': '🟠',
                'color': '#ffa502',
                'questions': important
            },
            {
                'name': 'Moderately Important Questions',
                'description': 'Questions that appeared once but contain key topics',
                'badge': '🟢',
                'color': '#2ed573',
                'questions': moderate
            }
        ],
        'summary': {
            'highly_important_count': len(highly_important),
            'important_count': len(important),
            'moderate_count': len(moderate)
        }
    }

    return report


# Testing
if __name__ == "__main__":
    print("=" * 60)
    print("QUESTION RANKER MODULE - TEST")
    print("=" * 60)

    # Sample data
    sample_groups = [
        {'representative': 'Explain OSI model', 'count': 5, 'variants': ['Explain OSI model', 'Describe OSI layers']},
        {'representative': 'What is TCP/IP?', 'count': 3, 'variants': ['What is TCP/IP?', 'Define TCP/IP']},
        {'representative': 'Define SQL', 'count': 1, 'variants': ['Define SQL']},
    ]

    sample_topic_analysis = {
        'top_keywords': [('model', 10), ('tcp', 8), ('osi', 7), ('sql', 5)],
        'question_analysis': [
            {'question': 'Explain OSI model', 'topic_score': 3},
            {'question': 'What is TCP/IP?', 'topic_score': 2},
            {'question': 'Define SQL', 'topic_score': 1},
        ]
    }

    ranked = rank_questions(sample_groups, sample_topic_analysis, total_papers=5)

    print("\n\nRanked Questions:")
    for q in ranked:
        print(f"\n{q['rank']}. {q['question']}")
        print(f"   Score: {q['importance_score']}, Frequency: {q['frequency']}")
        print(f"   Level: {q['classification']['label']}")

