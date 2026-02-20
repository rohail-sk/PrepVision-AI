"""
Question Paper Generator Module
Automatically generates predicted question papers from analyzed questions.
"""


def generate_predicted_paper(ranked_questions, top_keywords):
    """
    Generate a predicted question paper with three sections based on question importance.

    This function creates an exam-like structure with:
    - SECTION A: Short Answer Questions (5 questions)
    - SECTION B: Medium Answer Questions (5 questions)
    - SECTION C: Long Answer Questions (3 questions - highest priority)

    Selection Logic:
    - Highest ranked questions → Section C (most important)
    - Medium ranked questions → Section B
    - Remaining questions → Section A

    Args:
        ranked_questions: List of tuples (question, score, index) sorted by importance
        top_keywords: List of tuples (keyword, frequency) - used for context

    Returns:
        dict: Dictionary with three sections:
            {
                "section_a": [list of 5 short answer questions],
                "section_b": [list of 5 medium answer questions],
                "section_c": [list of 3 long answer questions]
            }
    """

    print("\n" + "="*50)
    print("Generating Predicted Question Paper")
    print("="*50)

    # Step 1: Remove duplicate questions while preserving ranking
    print("\nStep 1: Removing duplicate questions...")
    seen = set()
    unique_questions = []

    for question, score, idx in ranked_questions:
        # Normalize question for comparison (lowercase, strip whitespace)
        normalized = ' '.join(question.lower().split())

        # Only add if we haven't seen this question before
        if normalized not in seen and len(question.strip()) > 0:
            seen.add(normalized)
            unique_questions.append((question, score, idx))

    print(f"   Original questions: {len(ranked_questions)}")
    print(f"   Unique questions: {len(unique_questions)}")
    print(f"   Duplicates removed: {len(ranked_questions) - len(unique_questions)}")

    # Step 2: Define section sizes
    SECTION_C_SIZE = 3  # Long answer (most important)
    SECTION_B_SIZE = 5  # Medium answer
    SECTION_A_SIZE = 5  # Short answer

    total_needed = SECTION_A_SIZE + SECTION_B_SIZE + SECTION_C_SIZE
    print(f"\nStep 2: Section configuration")
    print(f"   Section A (Short): {SECTION_A_SIZE} questions")
    print(f"   Section B (Medium): {SECTION_B_SIZE} questions")
    print(f"   Section C (Long): {SECTION_C_SIZE} questions")
    print(f"   Total needed: {total_needed} questions")

    # Step 3: Handle edge case - not enough questions
    available = len(unique_questions)
    print(f"\nStep 3: Available questions: {available}")

    if available < total_needed:
        print(f"   ⚠️ Warning: Not enough questions ({available} < {total_needed})")
        print(f"   Adjusting section sizes proportionally...")

        # Adjust section sizes proportionally
        if available >= 3:
            # At least 3 questions - distribute proportionally
            SECTION_C_SIZE = min(SECTION_C_SIZE, max(1, available // 3))
            SECTION_B_SIZE = min(SECTION_B_SIZE, max(1, (available - SECTION_C_SIZE) // 2))
            SECTION_A_SIZE = available - SECTION_C_SIZE - SECTION_B_SIZE
        elif available == 2:
            # Only 2 questions
            SECTION_C_SIZE = 1
            SECTION_B_SIZE = 1
            SECTION_A_SIZE = 0
        elif available == 1:
            # Only 1 question
            SECTION_C_SIZE = 1
            SECTION_B_SIZE = 0
            SECTION_A_SIZE = 0
        else:
            # No questions available
            SECTION_C_SIZE = 0
            SECTION_B_SIZE = 0
            SECTION_A_SIZE = 0

        print(f"   Adjusted - Section A: {SECTION_A_SIZE}, Section B: {SECTION_B_SIZE}, Section C: {SECTION_C_SIZE}")

    # Step 4: Assign questions to sections based on ranking
    # Higher score = more important = goes to Section C (long answer)
    print("\nStep 4: Assigning questions to sections...")

    # Section C gets the TOP ranked questions (most important)
    section_c_start = 0
    section_c_end = SECTION_C_SIZE
    section_c = [q[0] for q in unique_questions[section_c_start:section_c_end]]
    print(f"   Section C: {len(section_c)} questions assigned (highest importance)")

    # Section B gets the NEXT ranked questions (medium importance)
    section_b_start = section_c_end
    section_b_end = section_b_start + SECTION_B_SIZE
    section_b = [q[0] for q in unique_questions[section_b_start:section_b_end]]
    print(f"   Section B: {len(section_b)} questions assigned (medium importance)")

    # Section A gets the REMAINING questions (lower importance but still relevant)
    section_a_start = section_b_end
    section_a_end = section_a_start + SECTION_A_SIZE
    section_a = [q[0] for q in unique_questions[section_a_start:section_a_end]]
    print(f"   Section A: {len(section_a)} questions assigned (lower importance)")

    # Step 5: Create structured dictionary
    predicted_paper = {
        "section_a": section_a,
        "section_b": section_b,
        "section_c": section_c
    }

    # Display summary
    print("\n" + "="*50)
    print("✅ Predicted Paper Generation Complete!")
    print("="*50)
    print(f"Total questions in predicted paper: {len(section_a) + len(section_b) + len(section_c)}")

    if len(section_c) > 0:
        print(f"\n📝 Section C Preview (Long Answer - Most Important):")
        for i, q in enumerate(section_c[:2], 1):
            preview = q[:70] + "..." if len(q) > 70 else q
            print(f"   {i}. {preview}")

    print("\n" + "="*50 + "\n")

    # Return the predicted paper structure
    return predicted_paper


# Testing function (runs only when this file is executed directly)
if __name__ == "__main__":
    print("="*60)
    print("QUESTION PAPER GENERATOR - TEST RUN")
    print("="*60)

    # Sample ranked questions for testing
    sample_ranked = [
        ("What is machine learning and explain its types?", 15.5, 1),
        ("Explain neural networks in detail", 14.2, 2),
        ("Define artificial intelligence", 13.8, 3),
        ("What are the applications of deep learning?", 12.5, 4),
        ("Explain supervised learning with examples", 11.3, 5),
        ("What is unsupervised learning?", 10.2, 6),
        ("Define reinforcement learning", 9.8, 7),
        ("Explain convolutional neural networks", 9.1, 8),
        ("What is natural language processing?", 8.5, 9),
        ("Define computer vision", 8.0, 10),
        ("Explain recurrent neural networks", 7.5, 11),
        ("What is transfer learning?", 7.0, 12),
        ("Define gradient descent", 6.5, 13),
    ]

    sample_keywords = [
        ("machine", 25),
        ("learning", 24),
        ("neural", 18),
        ("network", 17),
        ("data", 15)
    ]

    # Generate predicted paper
    paper = generate_predicted_paper(sample_ranked, sample_keywords)

    # Display results
    print("\n" + "="*60)
    print("GENERATED PREDICTED QUESTION PAPER")
    print("="*60)

    print("\n📘 SECTION A — Short Answer Questions")
    print("-"*60)
    for i, q in enumerate(paper['section_a'], 1):
        print(f"{i}. {q}")

    print("\n📗 SECTION B — Medium Answer Questions")
    print("-"*60)
    for i, q in enumerate(paper['section_b'], 1):
        print(f"{i}. {q}")

    print("\n📕 SECTION C — Long Answer Questions")
    print("-"*60)
    for i, q in enumerate(paper['section_c'], 1):
        print(f"{i}. {q}")

    print("\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*60)

