"""
Practice Paper Generator Module
Generates practice exam papers from analyzed questions.

IMPORTANT: This generates a PRACTICE paper based on PYQ analysis,
NOT a guaranteed prediction. The paper helps students focus on
frequently asked topics and question types.
"""


def generate_practice_paper(ranked_questions, config=None):
    """
    Generate a practice question paper from ranked questions.

    The paper is organized into three sections:
    - Section C: Long answer (most important questions)
    - Section B: Medium answer questions
    - Section A: Short answer questions

    Args:
        ranked_questions (list): Ranked questions from question_ranker module
        config (dict): Optional configuration for section sizes

    Returns:
        dict: Practice paper with sections and metadata
    """
    # Default configuration
    if config is None:
        config = {
            'section_c_size': 3,   # Long answer (10 marks each)
            'section_b_size': 5,   # Medium answer (6 marks each)
            'section_a_size': 5,   # Short answer (4 marks each)
        }

    print("\n" + "=" * 60)
    print("📝 PRACTICE PAPER GENERATION")
    print("=" * 60)

    # Get section sizes
    c_size = config['section_c_size']
    b_size = config['section_b_size']
    a_size = config['section_a_size']
    total_needed = c_size + b_size + a_size

    print(f"\nConfiguration:")
    print(f"  Section A (Short): {a_size} questions")
    print(f"  Section B (Medium): {b_size} questions")
    print(f"  Section C (Long):   {c_size} questions")
    print(f"  Total needed: {total_needed} questions")

    # Filter unique questions (avoid duplicates)
    seen_questions = set()
    unique_questions = []

    for q in ranked_questions:
        # Normalize for comparison
        normalized = ' '.join(q['question'].lower().split())

        if normalized not in seen_questions and len(q['question'].strip()) > 10:
            seen_questions.add(normalized)
            unique_questions.append(q)

    available = len(unique_questions)
    print(f"\nAvailable unique questions: {available}")

    # Adjust sizes if not enough questions
    if available < total_needed:
        print(f"⚠️ Adjusting section sizes (only {available} questions available)")

        if available >= 3:
            c_size = min(c_size, max(1, available // 3))
            b_size = min(b_size, max(1, (available - c_size) // 2))
            a_size = available - c_size - b_size
        elif available == 2:
            c_size, b_size, a_size = 1, 1, 0
        elif available == 1:
            c_size, b_size, a_size = 1, 0, 0
        else:
            c_size, b_size, a_size = 0, 0, 0

    # Assign questions to sections
    # Section C gets highest ranked (most important)
    section_c_questions = unique_questions[0:c_size]
    section_b_questions = unique_questions[c_size:c_size + b_size]
    section_a_questions = unique_questions[c_size + b_size:c_size + b_size + a_size]

    # Build section data
    def build_section(questions, marks_per_question):
        return [
            {
                'number': i + 1,
                'question': q['question'],
                'frequency': q.get('frequency', 1),
                'importance': q.get('classification', {}).get('label', 'Important'),
                'marks': marks_per_question
            }
            for i, q in enumerate(questions)
        ]

    section_a = build_section(section_a_questions, 4)
    section_b = build_section(section_b_questions, 6)
    section_c = build_section(section_c_questions, 10)

    # Calculate totals
    total_marks = (len(section_a) * 4) + (len(section_b) * 6) + (len(section_c) * 10)
    total_questions = len(section_a) + len(section_b) + len(section_c)

    print(f"\n✅ Practice Paper Generated:")
    print(f"  Section A: {len(section_a)} questions × 4 marks")
    print(f"  Section B: {len(section_b)} questions × 6 marks")
    print(f"  Section C: {len(section_c)} questions × 10 marks")
    print(f"  Total: {total_questions} questions, {total_marks} marks")

    # Build practice paper object
    practice_paper = {
        'title': 'Practice Question Paper',
        'subtitle': 'Based on Previous Year Question Analysis',
        'disclaimer': 'This is a practice paper generated from PYQ analysis. Questions are selected based on frequency and importance patterns.',
        'sections': {
            'section_a': {
                'name': 'SECTION A',
                'description': 'Short Answer Questions',
                'instruction': 'Answer any FIVE questions. Each question carries 4 marks.',
                'marks_each': 4,
                'questions': section_a
            },
            'section_b': {
                'name': 'SECTION B',
                'description': 'Medium Answer Questions',
                'instruction': 'Answer any FIVE questions. Each question carries 6 marks.',
                'marks_each': 6,
                'questions': section_b
            },
            'section_c': {
                'name': 'SECTION C',
                'description': 'Long Answer Questions',
                'instruction': 'Answer any THREE questions. Each question carries 10 marks.',
                'marks_each': 10,
                'questions': section_c
            }
        },
        'metadata': {
            'total_questions': total_questions,
            'total_marks': total_marks,
            'source_questions': len(ranked_questions),
            'unique_questions': available
        },
        # Legacy format for backwards compatibility
        'section_a': [q['question'] for q in section_a_questions],
        'section_b': [q['question'] for q in section_b_questions],
        'section_c': [q['question'] for q in section_c_questions]
    }

    return practice_paper


def generate_topic_wise_paper(ranked_questions, topic_analysis, questions_per_topic=2):
    """
    Generate a practice paper organized by topics.

    Args:
        ranked_questions (list): Ranked questions
        topic_analysis (dict): Topic analysis results
        questions_per_topic (int): Questions to include per topic

    Returns:
        dict: Topic-wise organized practice paper
    """
    print("\n" + "=" * 60)
    print("📝 TOPIC-WISE PRACTICE PAPER")
    print("=" * 60)

    questions_by_topic = topic_analysis.get('topic_frequency', {}).get('questions_by_topic', {})

    topic_sections = []
    total_questions = 0

    for topic, questions in questions_by_topic.items():
        if topic == 'general':
            continue

        # Sort questions by importance
        sorted_qs = sorted(questions, key=lambda x: x.get('score', 0), reverse=True)

        # Take top N questions for this topic
        selected = sorted_qs[:questions_per_topic]

        if selected:
            topic_sections.append({
                'topic': topic.replace('_', ' ').title(),
                'questions': [q['question'] for q in selected],
                'count': len(selected)
            })
            total_questions += len(selected)

    print(f"\n✅ Generated {len(topic_sections)} topic sections")
    print(f"   Total questions: {total_questions}")

    return {
        'title': 'Topic-Wise Practice Paper',
        'sections': topic_sections,
        'total_questions': total_questions
    }


# Testing
if __name__ == "__main__":
    print("=" * 60)
    print("PRACTICE PAPER GENERATOR - TEST")
    print("=" * 60)

    # Sample ranked questions
    sample_ranked = [
        {'question': 'Explain the OSI model in detail.', 'frequency': 5, 'classification': {'label': 'Highly Important'}},
        {'question': 'What is TCP/IP protocol?', 'frequency': 4, 'classification': {'label': 'Highly Important'}},
        {'question': 'Define machine learning.', 'frequency': 3, 'classification': {'label': 'Important'}},
        {'question': 'Explain neural networks.', 'frequency': 3, 'classification': {'label': 'Important'}},
        {'question': 'What is SQL?', 'frequency': 2, 'classification': {'label': 'Important'}},
        {'question': 'Define database normalization.', 'frequency': 2, 'classification': {'label': 'Important'}},
        {'question': 'Explain process scheduling.', 'frequency': 2, 'classification': {'label': 'Important'}},
        {'question': 'What is deadlock?', 'frequency': 2, 'classification': {'label': 'Important'}},
        {'question': 'Define inheritance in OOP.', 'frequency': 1, 'classification': {'label': 'Moderate'}},
        {'question': 'Explain polymorphism.', 'frequency': 1, 'classification': {'label': 'Moderate'}},
        {'question': 'What is encapsulation?', 'frequency': 1, 'classification': {'label': 'Moderate'}},
        {'question': 'Define abstraction.', 'frequency': 1, 'classification': {'label': 'Moderate'}},
        {'question': 'Explain data types.', 'frequency': 1, 'classification': {'label': 'Moderate'}},
    ]

    paper = generate_practice_paper(sample_ranked)

    print("\n\n" + "=" * 60)
    print("GENERATED PRACTICE PAPER")
    print("=" * 60)

    for section_key in ['section_c', 'section_b', 'section_a']:
        section = paper['sections'][section_key]
        print(f"\n{section['name']} — {section['description']}")
        print(f"({section['instruction']})")
        print("-" * 50)
        for q in section['questions']:
            print(f"{q['number']}. {q['question']} [{q['marks']} marks]")

