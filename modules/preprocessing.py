"""
NLP Preprocessing Module for Question Paper Analysis
This module provides functions to clean and extract questions from text.
"""
import re
import nltk
from collections import Counter
# Initialize NLTK components
def initialize_nltk():
    """
    Download required NLTK data if not already present.
    This function runs automatically when the module is imported.
    """
    # Try to download NLTK data
    required_data = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']

    for name in required_data:
        try:
            # Try to download quietly
            nltk.download(name, quiet=True)
        except Exception as e:
            print(f"Note: Could not download {name}. Will use fallback methods.")
            pass

# Initialize NLTK data when module is imported
try:
    initialize_nltk()
except:
    print("NLTK initialization had issues. Proceeding with fallback methods...")
    pass
# Import NLTK components after initialization
try:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    NLTK_AVAILABLE = True
except:
    print("NLTK components not fully available. Using fallback methods.")
    NLTK_AVAILABLE = False
def preprocess_text(raw_text):
    """
    Preprocess raw text by cleaning and tokenizing.
    This function performs the following NLP steps:
    1. Convert text to lowercase
    2. Remove special characters and numbers
    3. Tokenization (split into words)
    4. Remove English stopwords
    5. Perform lemmatization
    Args:
        raw_text (str): The raw extracted text from OCR
    Returns:
        tuple: (cleaned_text, list_of_tokens)
            - cleaned_text: The preprocessed text as a single string
            - list_of_tokens: List of cleaned tokens after lemmatization
    """
    if not raw_text or len(raw_text.strip()) == 0:
        return "", []
    # Step 1: Convert text to lowercase
    text = raw_text.lower()
    print("Step 1: Text converted to lowercase")
    # Step 2: Remove special characters and numbers
    # Keep only alphabets and spaces
    text = re.sub(r'[^a-z\s]', '', text)
    print("Step 2: Special characters and numbers removed")
    # Step 3: Tokenization - split into words
    try:
        tokens = word_tokenize(text)
        print(f"Step 3: Text tokenized into {len(tokens)} tokens")
    except:
        # Fallback to simple split if word_tokenize fails
        tokens = text.split()
        print(f"Step 3: Text split into {len(tokens)} tokens (fallback method)")
    # Step 4: Remove English stopwords
    try:
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
        print(f"Step 4: Stopwords removed. {len(filtered_tokens)} tokens remaining")
    except:
        # Fallback if stopwords not available
        filtered_tokens = [word for word in tokens if len(word) > 1]
        print(f"Step 4: Basic filtering applied (stopwords unavailable)")
    # Step 5: Perform lemmatization
    try:
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        print(f"Step 5: Lemmatization completed")
    except:
        # Fallback if lemmatizer not available
        lemmatized_tokens = filtered_tokens
        print(f"Step 5: Lemmatization skipped (unavailable)")
    # Create cleaned text from lemmatized tokens
    cleaned_text = ' '.join(lemmatized_tokens)
    return cleaned_text, lemmatized_tokens
def extract_questions(raw_text):
    """
    Extract individual questions from raw text using various patterns.
    This function identifies questions using these patterns:
    - Q1, Q2, Q3, etc. (with optional . : or ))
    - 1., 2., 3., etc.
    - Newline separation
    Args:
        raw_text (str): The raw extracted text from OCR
    Returns:
        list: List of extracted questions as strings
    """
    if not raw_text or len(raw_text.strip()) == 0:
        return []
    questions = []
    # Pattern 1: Match Q1, Q2, Q3, etc. (case insensitive)
    # Matches: Q1. Q2: Q3) Q4 followed by space
    pattern1 = r'Q\d+[\.\:\)\s]+'
    # Pattern 2: Match 1., 2., 3., etc.
    # Matches: 1. 2. 3. followed by space
    pattern2 = r'\d+\.\s+'
    # Pattern 3: Match Q1), Q2), etc.
    # Matches: Q1) Q2) Q3)
    pattern3 = r'Q\d+\)\s*'
    # Combine all patterns
    combined_pattern = f'({pattern1}|{pattern2}|{pattern3})'
    # Split text using the combined pattern
    parts = re.split(combined_pattern, raw_text, flags=re.IGNORECASE)
    # Filter out empty strings and pattern matches themselves
    for part in parts:
        # Skip if it's empty or just whitespace
        if not part or part.strip() == '':
            continue
        # Skip if it's just a question marker (Q1, 1., etc.)
        if re.match(combined_pattern, part.strip(), flags=re.IGNORECASE):
            continue
        # Clean up the question text
        question = part.strip()
        # Only add if it has substantial content (more than 10 characters)
        if len(question) > 10:
            questions.append(question)
    # If no questions found using patterns, try splitting by double newlines
    if len(questions) == 0:
        print("No questions found with standard patterns. Trying double newlines...")
        # Split by double newlines or multiple newlines
        parts = re.split(r'\n\s*\n', raw_text)
        questions = [q.strip() for q in parts if len(q.strip()) > 10]
    # If still no questions, try splitting by single newlines
    if len(questions) == 0:
        print("Trying single newline separation...")
        parts = raw_text.split('\n')
        questions = [q.strip() for q in parts if len(q.strip()) > 20]
    print(f"Extracted {len(questions)} questions from text")
    return questions
def analyze_text(raw_text):
    """
    Complete analysis function that combines preprocessing and question extraction.
    This is a convenience function that runs both preprocess_text() and
    extract_questions() and returns all results together.
    Args:
        raw_text (str): The raw extracted text from OCR
    Returns:
        dict: Dictionary containing:
            - cleaned_text: Preprocessed text
            - tokens: List of tokens
            - questions: List of extracted questions
            - question_count: Number of questions found
    """
    print("\n" + "="*50)
    print("Starting Text Analysis")
    print("="*50)
    # Preprocess the text
    print("\n>>> Running Preprocessing...")
    cleaned_text, tokens = preprocess_text(raw_text)
    # Extract questions
    print("\n>>> Extracting Questions...")
    questions = extract_questions(raw_text)
    # Return all results in a dictionary
    result = {
        'cleaned_text': cleaned_text,
        'tokens': tokens,
        'questions': questions,
        'question_count': len(questions)
    }
    print("\n" + "="*50)
    print("Analysis Complete!")
    print(f"Total Tokens: {len(tokens)}")
    print(f"Total Questions: {len(questions)}")
    print("="*50 + "\n")
    return result


def analyze_topics(tokens, questions):
    """
    Analyze topics from tokens and rank questions by importance.

    This function performs:
    1. Word frequency analysis using collections.Counter
    2. Filters out very short words (length < 3)
    3. Identifies most common keywords/topics
    4. Scores each question based on high-frequency keywords

    Args:
        tokens (list): List of preprocessed tokens from preprocess_text()
        questions (list): List of questions from extract_questions()

    Returns:
        dict: Dictionary containing:
            - top_keywords: List of tuples (word, frequency) - most common words
            - ranked_questions: List of tuples (question, score, index) - sorted by importance
            - keyword_count: Total number of unique keywords
            - avg_score: Average importance score
    """

    # Validate inputs
    if not tokens or len(tokens) == 0:
        print("Warning: No tokens provided for analysis")
        return {
            'top_keywords': [],
            'ranked_questions': [],
            'keyword_count': 0,
            'avg_score': 0
        }

    if not questions or len(questions) == 0:
        print("Warning: No questions provided for ranking")
        return {
            'top_keywords': [],
            'ranked_questions': [],
            'keyword_count': 0,
            'avg_score': 0
        }

    print("\n" + "="*50)
    print("Starting Topic Analysis")
    print("="*50)

    # Step 1: Filter tokens - remove very short words (length < 3)
    # Short words like "is", "of", "it" don't carry much meaning
    filtered_tokens = [word for word in tokens if len(word) >= 3]
    print(f"Step 1: Filtered tokens. {len(filtered_tokens)} meaningful words (length >= 3)")

    # Step 2: Word frequency analysis using Counter
    # Counter counts how many times each word appears
    word_freq = Counter(filtered_tokens)
    print(f"Step 2: Word frequency calculated. {len(word_freq)} unique words found")

    # Step 3: Get top keywords (most common words)
    # most_common(n) returns top n words as list of (word, count) tuples
    top_keywords = word_freq.most_common(10)  # Get top 10 keywords
    print(f"Step 3: Top keywords identified")

    # Display top keywords
    print("\n📊 Top Keywords Found:")
    for i, (word, freq) in enumerate(top_keywords, 1):
        print(f"  {i}. '{word}' - appears {freq} times")

    # Step 4: Create importance scoring for questions
    # Questions containing more high-frequency keywords are considered more important
    print(f"\nStep 4: Scoring {len(questions)} questions...")

    # Get top keyword words only (without frequencies)
    top_keyword_words = set([word for word, freq in top_keywords])

    # Score each question
    question_scores = []
    for idx, question in enumerate(questions):
        # Convert question to lowercase for matching
        question_lower = question.lower()

        # Remove special characters from question
        question_clean = re.sub(r'[^a-z\s]', '', question_lower)

        # Split question into words
        question_words = question_clean.split()

        # Calculate score: count how many top keywords appear in this question
        score = 0
        for word in question_words:
            if word in top_keyword_words:
                score += 1

        # Also give bonus points based on overall word frequency
        for word in question_words:
            if word in word_freq and len(word) >= 3:
                # Add frequency weight (normalized)
                score += word_freq[word] * 0.1

        # Store: (question, score, original_index)
        question_scores.append((question, score, idx + 1))

    # Step 5: Sort questions by importance score (highest first)
    ranked_questions = sorted(question_scores, key=lambda x: x[1], reverse=True)
    print(f"Step 5: Questions ranked by importance")

    # Calculate average score
    avg_score = sum([score for _, score, _ in ranked_questions]) / len(ranked_questions) if ranked_questions else 0

    # Display top ranked questions
    print("\n🏆 Top Ranked Questions:")
    for i, (question, score, idx) in enumerate(ranked_questions[:5], 1):
        preview = question[:80] + "..." if len(question) > 80 else question
        print(f"  {i}. [Score: {score:.2f}] Q{idx}: {preview}")

    print("\n" + "="*50)
    print("Topic Analysis Complete!")
    print("="*50)

    # Return results
    return {
        'top_keywords': top_keywords,
        'ranked_questions': ranked_questions,
        'keyword_count': len(word_freq),
        'avg_score': avg_score
    }


# Example usage and testing (runs only when script is executed directly)
if __name__ == "__main__":
    # Sample text for testing
    sample_text = """
    Q1. What is machine learning?
    Machine learning is a subset of artificial intelligence.
    Q2. Explain the concept of neural networks.
    Neural networks are computing systems inspired by biological neural networks.
    Q3. Define artificial intelligence and its applications.
    AI is the simulation of human intelligence by machines.
    1. What are the types of machine learning?
    2. Explain supervised learning.
    3. What is deep learning?
    """
    print("="*60)
    print("NLP PREPROCESSING MODULE - TEST RUN")
    print("="*60)
    # Test 1: preprocess_text function
    print("\n\nTEST 1: PREPROCESS_TEXT FUNCTION")
    print("-"*60)
    cleaned, tokens = preprocess_text(sample_text)
    print("\nCLEANED TEXT:")
    print(cleaned[:200] + "..." if len(cleaned) > 200 else cleaned)
    print(f"\nTOKENS (first 20): {tokens[:20]}")
    # Test 2: extract_questions function
    print("\n\nTEST 2: EXTRACT_QUESTIONS FUNCTION")
    print("-"*60)
    questions = extract_questions(sample_text)
    print("\nEXTRACTED QUESTIONS:")
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}:")
        print(f"  {q[:100]}..." if len(q) > 100 else f"  {q}")
    # Test 3: analyze_text function (complete analysis)
    print("\n\nTEST 3: ANALYZE_TEXT FUNCTION (COMPLETE ANALYSIS)")
    print("-"*60)
    result = analyze_text(sample_text)
    print("\nRESULTS SUMMARY:")
    print(f"  - Question Count: {result['question_count']}")
    print(f"  - Token Count: {len(result['tokens'])}")
    print(f"  - Cleaned Text Length: {len(result['cleaned_text'])} characters")

    # Test 4: analyze_topics function (topic analysis and ranking)
    print("\n\nTEST 4: ANALYZE_TOPICS FUNCTION (TOPIC ANALYSIS & RANKING)")
    print("-"*60)
    topic_result = analyze_topics(tokens, questions)
    print("\nTOPIC ANALYSIS RESULTS:")
    print(f"  - Unique Keywords: {topic_result['keyword_count']}")
    print(f"  - Average Question Score: {topic_result['avg_score']:.2f}")
    print(f"\n  Top 5 Keywords:")
    for word, freq in topic_result['top_keywords'][:5]:
        print(f"    • {word}: {freq} occurrences")
    print(f"\n  Top 3 Important Questions:")
    for i, (question, score, idx) in enumerate(topic_result['ranked_questions'][:3], 1):
        preview = question[:60] + "..." if len(question) > 60 else question
        print(f"    {i}. [Score: {score:.1f}] {preview}")

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)
