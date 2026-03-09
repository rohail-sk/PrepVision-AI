"""
Text Cleaner Module
Removes instruction phrases, page markers, and noise from extracted text.
"""

import re


# Instruction phrases that should be removed from questions
INSTRUCTION_PATTERNS = [
    r'attempt\s+any\s*\d*\s*(questions?)?',
    r'answer\s+(any|all|the\s+following)\s*\d*\s*(questions?)?',
    r'marks?\s*[:=]?\s*\d+',
    r'\d+\s*marks?',
    r'p\.?\s*t\.?\s*o\.?',
    r'page\s*[-:]?\s*\d+',
    r'time\s*[:=]?\s*\d+\s*(hours?|hrs?|minutes?|mins?)?',
    r'max(imum)?\s*marks?\s*[:=]?\s*\d+',
    r'total\s*marks?\s*[:=]?\s*\d+',
    r'instructions?\s*[:=]?',
    r'note\s*[:=]?',
    r'---\s*page\s*\d+\s*---',
    r'\[\s*\d+\s*marks?\s*\]',
    r'\(\s*\d+\s*marks?\s*\)',
    r'q\.?\s*no\.?',
    r'question\s*no\.?',
    r'roll\s*no\.?',
    r'seat\s*no\.?',
    r'exam(ination)?\s*[:=]?',
    r'subject\s*[:=]?',
    r'course\s*[:=]?',
    r'date\s*[:=]?',
    r'duration\s*[:=]?',
    r'or\s*$',  # Trailing "OR" at end of questions
    r'^\s*or\s*',  # Leading "OR" at start
]

# Compiled patterns for efficiency
COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in INSTRUCTION_PATTERNS]


def clean_instruction_noise(text):
    """
    Remove instruction phrases and exam metadata from text.

    Args:
        text (str): Raw extracted text

    Returns:
        str: Cleaned text with instructions removed
    """
    if not text:
        return ""

    cleaned = text

    # Apply all instruction removal patterns
    for pattern in COMPILED_PATTERNS:
        cleaned = pattern.sub(' ', cleaned)

    # Remove multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()

    return cleaned


def clean_question_text(question):
    """
    Clean a single question by removing instruction noise.

    Args:
        question (str): Raw question text

    Returns:
        str: Cleaned question text
    """
    if not question:
        return ""

    # Remove instruction noise
    cleaned = clean_instruction_noise(question)

    # Remove question numbers at the start (Q1, Q2, 1., 2., etc.)
    cleaned = re.sub(r'^[Qq]?\d+[\.\)\:]?\s*', '', cleaned)

    # Remove sub-question markers (a), b), i), ii), etc.)
    cleaned = re.sub(r'^[a-z][\.\)]\s*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'^[ivx]+[\.\)]\s*', '', cleaned, flags=re.IGNORECASE)

    # Capitalize first letter
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned.upper()

    return cleaned.strip()


def remove_page_headers_footers(text):
    """
    Remove common page headers and footers from extracted text.

    Args:
        text (str): Raw text with headers/footers

    Returns:
        str: Text with headers/footers removed
    """
    if not text:
        return ""

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line_lower = line.lower().strip()

        # Skip common header/footer patterns
        skip_patterns = [
            'page',
            'p.t.o',
            'turn over',
            'continued',
            'www.',
            'http',
            'copyright',
            'all rights reserved',
        ]

        # Check if line should be skipped
        should_skip = False
        for pattern in skip_patterns:
            if pattern in line_lower and len(line_lower) < 50:
                should_skip = True
                break

        if not should_skip:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def is_valid_question(question, min_length=15):
    """
    Check if a question is valid (not just noise or metadata).

    Args:
        question (str): Question text to validate
        min_length (int): Minimum character length for valid question

    Returns:
        bool: True if question is valid
    """
    if not question:
        return False

    cleaned = clean_question_text(question)

    # Check minimum length
    if len(cleaned) < min_length:
        return False

    # Check if it's mostly numbers or special characters
    alpha_count = sum(1 for c in cleaned if c.isalpha())
    if alpha_count < len(cleaned) * 0.5:
        return False

    # Check for common non-question patterns
    invalid_patterns = [
        r'^(name|roll|seat|date|time|marks?|total|max)\s*[:=]?$',
        r'^\d+$',
        r'^[a-z]$',
    ]

    for pattern in invalid_patterns:
        if re.match(pattern, cleaned, re.IGNORECASE):
            return False

    return True


# Testing
if __name__ == "__main__":
    print("=" * 60)
    print("TEXT CLEANER MODULE - TEST")
    print("=" * 60)

    test_questions = [
        "Q1. Explain the OSI model in detail. [6 Marks]",
        "2) What is TCP/IP? Attempt any 2.",
        "Answer the following: Define machine learning.",
        "P.T.O.",
        "Page 5",
        "Marks: 100",
    ]

    print("\nCleaning test questions:\n")
    for q in test_questions:
        cleaned = clean_question_text(q)
        valid = is_valid_question(q)
        print(f"Original: {q}")
        print(f"Cleaned:  {cleaned}")
        print(f"Valid:    {valid}")
        print("-" * 40)

