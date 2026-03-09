"""
Question Extractor Module
Extracts ONLY actual questions from question papers.
Filters out instructions, exam codes, page numbers, and formatting text.
"""

import re
from collections import Counter


# ══════════════════════════════════════════════════════════════════════════════
# INSTRUCTION PATTERNS TO FILTER OUT
# ══════════════════════════════════════════════════════════════════════════════

INSTRUCTION_PATTERNS = [
    # General exam instructions
    r'all\s+questions?\s+are\s+compulsory',
    r'answer\s+(any|all|each|the\s+following)',
    r'attempt\s+(any|all)\s*\d*\s*(questions?)?',
    r'answer\s+each\s+next\s+main\s+question',
    r'figures?\s+to\s+the\s+right\s+indicate',
    r'assume\s+suitable\s+data',
    r'draw\s+neat\s+(and\s+clean\s+)?diagrams?',
    r'use\s+of\s+(non[- ]?programmable\s+)?calculator',
    r'mobile\s+phones?\s+(are\s+)?(not\s+)?allowed',
    r'use\s+of\s+electronic?\s+gadgets?',

    # Time and marks indicators
    r'\d+\s*hours?',
    r'\d+\s*hrs?',
    r'\d+\s*minutes?',
    r'\d+\s*mins?',
    r'time\s*[:=]?\s*\d+',
    r'duration\s*[:=]?\s*\d+',
    r'max(imum)?\s*marks?\s*[:=]?\s*\d+',
    r'total\s*marks?\s*[:=]?\s*\d+',
    r'\[\s*\d+\s*\]',  # [2], [3], [4] marks
    r'\(\s*\d+\s*\)',  # (2), (3), (4) marks
    r'\d+\s*marks?',
    r'marks?\s*[:=]?\s*\d+',

    # Page indicators
    r'page\s*[-:]?\s*\d+',
    r'p\.?\s*t\.?\s*o\.?',
    r'turn\s+over',
    r'continued',
    r'---+',
    r'___+',
    r'\*{3,}',

    # Exam metadata
    r'exam(ination)?\s*(code)?[:=]?',
    r'subject\s*(code)?[:=]?',
    r'course\s*(code)?[:=]?',
    r'paper\s*(code|id)?[:=]?',
    r'seat\s*no\.?[:=]?',
    r'roll\s*no\.?[:=]?',
    r'enrolment\s*no\.?',
    r'reg(istration)?\s*no\.?',
    r'date\s*[:=]?',
    r'semester\s*[:=]?',
    r'year\s*[:=]?',
    r'branch\s*[:=]?',
    r'division\s*[:=]?',

    # Section headers
    r'^section\s*[-:]?\s*[a-z]$',
    r'^part\s*[-:]?\s*[a-z]$',
    r'^unit\s*[-:]?\s*\d+$',
    r'^module\s*[-:]?\s*\d+$',

    # Instructions keywords
    r'^instructions?\s*[:=]?',
    r'^note\s*[:=]?',
    r'^important\s*[:=]?',
    r'read\s+(the\s+)?instructions?\s+carefully',
    r'follow\s+the\s+instructions?',

    # Miscellaneous noise
    r'^or$',
    r'^and$',
    r'^\d+$',  # Just numbers
    r'^[a-z]$',  # Just single letters
    r'government\s+of\s+',
    r'board\s+of\s+',
    r'technical\s+education',
    r'maharashtra\s+state',
    r'msbte',
    r'winter|summer|monsoon',
    r'examination',
]

# Exam codes pattern (5-6 digit numbers like 22519, 312303)
EXAM_CODE_PATTERN = r'^\d{5,6}$'

# Compile all patterns for efficiency
COMPILED_INSTRUCTION_PATTERNS = [re.compile(p, re.IGNORECASE) for p in INSTRUCTION_PATTERNS]
COMPILED_EXAM_CODE = re.compile(EXAM_CODE_PATTERN)


# ══════════════════════════════════════════════════════════════════════════════
# QUESTION DETECTION PATTERNS
# ══════════════════════════════════════════════════════════════════════════════

# Question starter patterns (sub-questions)
SUBQUESTION_PATTERN = re.compile(r'^[a-f][\.\)]\s*', re.IGNORECASE)
ROMAN_SUBQUESTION_PATTERN = re.compile(r'^[ivx]+[\.\)]\s*', re.IGNORECASE)

# Question verb keywords that indicate actual questions
QUESTION_VERBS = [
    'explain', 'define', 'describe', 'discuss', 'write', 'develop',
    'state', 'list', 'compare', 'differentiate', 'distinguish',
    'what', 'why', 'how', 'when', 'where', 'which', 'who',
    'enumerate', 'illustrate', 'derive', 'prove', 'solve',
    'calculate', 'compute', 'find', 'determine', 'evaluate',
    'draw', 'sketch', 'design', 'implement', 'create',
    'convert', 'construct', 'demonstrate', 'elaborate', 'classify',
    'identify', 'mention', 'name', 'give', 'provide',
    'analyze', 'examine', 'assess', 'justify', 'outline'
]

QUESTION_VERB_PATTERN = re.compile(
    r'\b(' + '|'.join(QUESTION_VERBS) + r')\b',
    re.IGNORECASE
)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def is_instruction_line(text):
    """
    Check if a line is an instruction/metadata rather than a question.

    Args:
        text (str): Line of text to check

    Returns:
        bool: True if it's an instruction line, False if it might be a question
    """
    if not text:
        return True

    text_clean = text.strip()
    text_lower = text_clean.lower()

    # Check against all instruction patterns
    for pattern in COMPILED_INSTRUCTION_PATTERNS:
        if pattern.search(text_lower):
            return True

    # Check if it's an exam code (5-6 digit number)
    if COMPILED_EXAM_CODE.match(text_clean):
        return True

    # Check if it's just a number with brackets like [2], [4]
    if re.match(r'^\[\s*\d+\s*\]$', text_clean):
        return True

    # Check if it's mostly numbers (>70% digits)
    if text_clean:
        digit_ratio = sum(c.isdigit() for c in text_clean) / len(text_clean)
        if digit_ratio > 0.7:
            return True

    return False


def is_valid_question(text, min_length=5, max_length=400):
    """
    Check if a line looks like an actual question.

    Args:
        text (str): Text to validate
        min_length (int): Minimum length for valid question
        max_length (int): Maximum length for valid question

    Returns:
        bool: True if it's a valid question
    """
    if not text:
        return False

    text_clean = text.strip()

    # Length check
    if len(text_clean) < min_length or len(text_clean) > max_length:
        return False

    # Must have at least some alphabetic characters (>50%)
    alpha_count = sum(c.isalpha() for c in text_clean)
    if len(text_clean) > 0 and alpha_count / len(text_clean) < 0.5:
        return False

    # Check if it's an instruction
    if is_instruction_line(text_clean):
        return False

    # Check for question indicators
    has_question_verb = bool(QUESTION_VERB_PATTERN.search(text_clean))
    has_subquestion_marker = bool(SUBQUESTION_PATTERN.match(text_clean)) or bool(ROMAN_SUBQUESTION_PATTERN.match(text_clean))
    ends_with_question_mark = text_clean.endswith('?')

    # A valid question should have at least one indicator
    if has_question_verb or has_subquestion_marker or ends_with_question_mark:
        return True

    # Also accept lines that start with capital letter and have reasonable content
    if text_clean[0].isupper() and len(text_clean) > 15 and alpha_count > 10:
        # Check if it contains meaningful words (not just random text)
        words = text_clean.split()
        if len(words) >= 3:
            return True

    return False


def extract_questions_advanced(raw_text):
    """
    Extract ONLY actual questions from raw text, filtering out all instructions.

    This function:
    1. Splits text into lines
    2. Filters out instruction lines
    3. Identifies question patterns
    4. Returns only valid questions

    Args:
        raw_text (str): Raw extracted text from OCR/PDF

    Returns:
        dict: Contains:
            - questions: List of extracted questions
            - removed_lines: List of filtered instruction lines
            - stats: Statistics about extraction
    """
    if not raw_text or len(raw_text.strip()) == 0:
        return {
            'questions': [],
            'removed_lines': [],
            'stats': {'total_lines': 0, 'questions_found': 0, 'removed_count': 0}
        }

    print("\n" + "=" * 60)
    print("📝 ADVANCED QUESTION EXTRACTION")
    print("=" * 60)

    # Split into lines
    lines = raw_text.split('\n')
    total_lines = len(lines)

    questions = []
    removed_lines = []

    # First pass: Extract by question number patterns
    # Pattern for main questions: Q1, Q2, 1., 2., etc.
    main_question_pattern = re.compile(r'^[Qq]?\s*\d+[\.\)\:]?\s*(.+)', re.MULTILINE)

    # Pattern for sub-questions: a), b), c), i), ii), etc.
    sub_question_pattern = re.compile(r'^[a-f][\.\)]\s*(.+)', re.IGNORECASE)
    roman_pattern = re.compile(r'^[ivx]+[\.\)]\s*(.+)', re.IGNORECASE)

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip very short lines
        if len(line) < 5:
            removed_lines.append(f"[TOO SHORT] {line}")
            continue

        # Skip very long lines (likely paragraphs or instructions)
        if len(line) > 400:
            removed_lines.append(f"[TOO LONG] {line[:50]}...")
            continue

        # Check if it's an instruction line
        if is_instruction_line(line):
            removed_lines.append(f"[INSTRUCTION] {line}")
            continue

        # Check if it's a valid question
        if is_valid_question(line):
            # Clean the question text
            cleaned = clean_question_for_output(line)
            if cleaned and len(cleaned) >= 5:
                questions.append(cleaned)
        else:
            removed_lines.append(f"[NOT QUESTION] {line}")

    # Remove duplicates while preserving order
    seen = set()
    unique_questions = []
    for q in questions:
        q_normalized = ' '.join(q.lower().split())
        if q_normalized not in seen:
            seen.add(q_normalized)
            unique_questions.append(q)

    # Statistics
    stats = {
        'total_lines': total_lines,
        'questions_found': len(unique_questions),
        'removed_count': len(removed_lines),
        'duplicates_removed': len(questions) - len(unique_questions)
    }

    # Print summary
    print(f"\n📊 EXTRACTION STATISTICS:")
    print(f"   Total lines processed: {stats['total_lines']}")
    print(f"   Questions extracted: {stats['questions_found']}")
    print(f"   Instruction lines removed: {stats['removed_count']}")
    print(f"   Duplicates removed: {stats['duplicates_removed']}")

    if unique_questions:
        print(f"\n📝 SAMPLE EXTRACTED QUESTIONS:")
        for i, q in enumerate(unique_questions[:5], 1):
            preview = q[:80] + "..." if len(q) > 80 else q
            print(f"   {i}. {preview}")

    if removed_lines:
        print(f"\n🗑️ SAMPLE REMOVED LINES:")
        for line in removed_lines[:5]:
            preview = line[:70] + "..." if len(line) > 70 else line
            print(f"   • {preview}")

    print("\n" + "=" * 60)

    return {
        'questions': unique_questions,
        'removed_lines': removed_lines,
        'stats': stats
    }


def clean_question_for_output(text):
    """
    Clean a question for final output.

    Args:
        text (str): Raw question text

    Returns:
        str: Cleaned question text
    """
    if not text:
        return ""

    cleaned = text.strip()

    # Remove leading question numbers (Q1, Q2, 1., 2., etc.)
    cleaned = re.sub(r'^[Qq]?\s*\d+[\.\)\:]?\s*', '', cleaned)

    # Remove sub-question markers at start if they're the only content
    # But keep them if there's content after
    if re.match(r'^[a-f][\.\)]\s*$', cleaned, re.IGNORECASE):
        return ""

    # Remove trailing marks indicators
    cleaned = re.sub(r'\s*\[\s*\d+\s*\]\s*$', '', cleaned)
    cleaned = re.sub(r'\s*\(\s*\d+\s*\)\s*$', '', cleaned)
    cleaned = re.sub(r'\s*\d+\s*marks?\s*$', '', cleaned, flags=re.IGNORECASE)

    # Remove multiple spaces
    cleaned = ' '.join(cleaned.split())

    # Capitalize first letter
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:] if len(cleaned) > 1 else cleaned.upper()

    return cleaned.strip()


def filter_questions_list(questions):
    """
    Filter an existing list of questions to remove instructions.

    Args:
        questions (list): List of question strings

    Returns:
        dict: Filtered questions with stats
    """
    if not questions:
        return {
            'questions': [],
            'removed': [],
            'stats': {'original': 0, 'filtered': 0, 'removed': 0}
        }

    filtered = []
    removed = []

    for q in questions:
        if is_valid_question(q) and not is_instruction_line(q):
            cleaned = clean_question_for_output(q)
            if cleaned and len(cleaned) >= 5:
                filtered.append(cleaned)
            else:
                removed.append(f"[EMPTY AFTER CLEAN] {q}")
        else:
            removed.append(f"[FILTERED] {q}")

    return {
        'questions': filtered,
        'removed': removed,
        'stats': {
            'original': len(questions),
            'filtered': len(filtered),
            'removed': len(removed)
        }
    }


# ══════════════════════════════════════════════════════════════════════════════
# TESTING
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("QUESTION EXTRACTOR MODULE - TEST")
    print("=" * 70)

    # Sample text with mixed content (instructions + questions)
    sample_text = """
    22519
    MAHARASHTRA STATE BOARD OF TECHNICAL EDUCATION
    Summer 2024 Examination
    
    Subject: Programming in C
    Duration: 3 Hours
    Max Marks: 70
    
    Instructions:
    1. All questions are compulsory
    2. Figures to the right indicate full marks
    3. Mobile phones are not allowed
    4. Assume suitable data if necessary
    
    Q1. Attempt any FIVE of the following: [10]
    a) Define Array. [2]
    b) Explain printf() and scanf() functions. [2]
    c) List the data types in C. [2]
    d) Write syntax of if-else statement. [2]
    e) State the use of break statement. [2]
    f) What is pointer? [2]
    
    Q2. Attempt any THREE of the following: [12]
    a) Write a program to reverse a given number. [4]
    b) Explain pointer to function with example. [4]
    c) Describe the structure of C program. [4]
    d) Compare while and do-while loop. [4]
    
    Q3. Attempt any THREE of the following: [12]
    a) Develop a program to find factorial of a number. [4]
    b) Discuss different storage classes in C. [4]
    
    [2]
    P.T.O.
    
    Page 2
    
    c) What is recursion? Explain with example. [4]
    d) Write a program to implement bubble sort. [4]
    
    ---
    312303
    """

    result = extract_questions_advanced(sample_text)

    print("\n\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print(f"\n✅ Total Questions Extracted: {result['stats']['questions_found']}")

    print("\n📝 All Extracted Questions:")
    for i, q in enumerate(result['questions'], 1):
        print(f"   {i}. {q}")

    print(f"\n🗑️ Removed Lines Count: {result['stats']['removed_count']}")

