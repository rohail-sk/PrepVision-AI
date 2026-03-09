"""
Topic Analysis Module
Clusters questions by topic and analyzes topic frequency.
Uses keyword extraction and optional LDA topic modeling.
"""

import re
from collections import Counter, defaultdict

# Try to import sklearn for advanced topic modeling
try:
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# Common exam topics/categories for technical subjects
TOPIC_KEYWORDS = {
    'networking': ['network', 'tcp', 'ip', 'osi', 'protocol', 'router', 'switch', 'lan', 'wan', 'ethernet', 'dns', 'dhcp', 'http', 'ftp', 'socket'],
    'database': ['database', 'sql', 'query', 'table', 'normalization', 'dbms', 'rdbms', 'key', 'join', 'index', 'transaction', 'acid'],
    'programming': ['function', 'variable', 'loop', 'array', 'pointer', 'class', 'object', 'inheritance', 'polymorphism', 'encapsulation', 'algorithm'],
    'web': ['html', 'css', 'javascript', 'web', 'browser', 'server', 'client', 'api', 'rest', 'json', 'xml', 'ajax'],
    'security': ['security', 'encryption', 'decryption', 'cipher', 'authentication', 'authorization', 'firewall', 'malware', 'virus', 'attack'],
    'operating_system': ['process', 'thread', 'memory', 'scheduling', 'deadlock', 'semaphore', 'mutex', 'paging', 'segmentation', 'kernel'],
    'machine_learning': ['machine', 'learning', 'neural', 'network', 'classification', 'regression', 'clustering', 'training', 'model', 'algorithm'],
    'data_structures': ['stack', 'queue', 'tree', 'graph', 'linked', 'list', 'sorting', 'searching', 'hash', 'heap', 'binary'],
}


def extract_keywords_from_question(question, top_n=5):
    """
    Extract important keywords from a question.

    Args:
        question (str): Question text
        top_n (int): Number of top keywords to return

    Returns:
        list: List of important keywords
    """
    if not question:
        return []

    # Normalize text
    text = question.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()

    # Filter stopwords and short words
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
                 'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
                 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
                 'below', 'between', 'under', 'again', 'further', 'then', 'once', 'here',
                 'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few', 'more',
                 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'what',
                 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'and',
                 'but', 'if', 'or', 'because', 'until', 'while', 'although', 'explain',
                 'define', 'describe', 'discuss', 'write', 'state', 'list', 'give',
                 'mention', 'note', 'brief', 'detail', 'example', 'examples'}

    keywords = [w for w in words if w not in stopwords and len(w) >= 3]

    # Count frequency within this question
    word_counts = Counter(keywords)

    return [word for word, count in word_counts.most_common(top_n)]


def identify_question_topic(question):
    """
    Identify the topic category of a question.

    Args:
        question (str): Question text

    Returns:
        tuple: (topic_name, confidence_score)
    """
    if not question:
        return ('general', 0)

    text_lower = question.lower()

    topic_scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            topic_scores[topic] = score

    if topic_scores:
        best_topic = max(topic_scores, key=topic_scores.get)
        return (best_topic, topic_scores[best_topic])

    return ('general', 0)


def analyze_topic_frequency(questions):
    """
    Analyze topic frequency across all questions.

    Args:
        questions (list): List of question strings

    Returns:
        dict: Topic analysis results containing:
            - topic_counts: Counter of topic frequencies
            - questions_by_topic: Questions grouped by topic
            - top_topics: List of (topic, count) sorted by frequency
    """
    topic_counts = Counter()
    questions_by_topic = defaultdict(list)

    for q in questions:
        topic, score = identify_question_topic(q)
        topic_counts[topic] += 1
        questions_by_topic[topic].append({
            'question': q,
            'score': score
        })

    top_topics = topic_counts.most_common(10)

    return {
        'topic_counts': dict(topic_counts),
        'questions_by_topic': dict(questions_by_topic),
        'top_topics': top_topics
    }


def extract_global_keywords(questions, top_n=20):
    """
    Extract the most common keywords across all questions.

    Args:
        questions (list): List of question strings
        top_n (int): Number of top keywords to return

    Returns:
        list: List of (keyword, frequency) tuples
    """
    all_keywords = []

    for q in questions:
        keywords = extract_keywords_from_question(q, top_n=10)
        all_keywords.extend(keywords)

    keyword_counts = Counter(all_keywords)

    return keyword_counts.most_common(top_n)


def perform_lda_topic_modeling(questions, n_topics=5):
    """
    Perform LDA topic modeling on questions.

    This is an advanced technique that discovers latent topics
    in the question corpus.

    Args:
        questions (list): List of question strings
        n_topics (int): Number of topics to discover

    Returns:
        dict: LDA results or None if sklearn unavailable
    """
    if not SKLEARN_AVAILABLE or len(questions) < n_topics:
        return None

    try:
        # Create document-term matrix
        vectorizer = CountVectorizer(
            max_df=0.95,
            min_df=2,
            stop_words='english',
            max_features=1000
        )

        doc_term_matrix = vectorizer.fit_transform(questions)

        # Fit LDA model
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=10
        )

        lda.fit(doc_term_matrix)

        # Get feature names (words)
        feature_names = vectorizer.get_feature_names_out()

        # Extract top words for each topic
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[:-10:-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics.append({
                'topic_id': topic_idx,
                'top_words': top_words
            })

        # Assign questions to topics
        topic_assignments = lda.transform(doc_term_matrix)

        return {
            'topics': topics,
            'assignments': topic_assignments.argmax(axis=1).tolist()
        }

    except Exception as e:
        print(f"LDA topic modeling error: {e}")
        return None


def comprehensive_topic_analysis(questions, total_papers=1):
    """
    Perform comprehensive topic analysis on questions.

    This function combines:
    1. Keyword extraction
    2. Topic categorization
    3. Frequency analysis
    4. Optional LDA modeling

    Args:
        questions (list): List of question strings
        total_papers (int): Number of papers analyzed

    Returns:
        dict: Comprehensive analysis results
    """
    print("\n" + "=" * 50)
    print("📊 TOPIC ANALYSIS")
    print("=" * 50)

    # Extract global keywords
    print("\n1. Extracting keywords...")
    top_keywords = extract_global_keywords(questions)
    print(f"   Found {len(top_keywords)} top keywords")

    # Analyze topic frequency
    print("\n2. Analyzing topic distribution...")
    topic_freq = analyze_topic_frequency(questions)
    print(f"   Found {len(topic_freq['top_topics'])} topic categories")

    # Try LDA topic modeling
    print("\n3. Attempting LDA topic modeling...")
    lda_results = perform_lda_topic_modeling(questions)
    if lda_results:
        print(f"   ✅ LDA discovered {len(lda_results['topics'])} topics")
    else:
        print(f"   ⚠️ LDA not available or insufficient data")

    # Build question importance data
    print("\n4. Calculating question importance...")
    question_analysis = []
    for i, q in enumerate(questions):
        keywords = extract_keywords_from_question(q)
        topic, topic_score = identify_question_topic(q)

        # Calculate importance based on keyword frequency
        importance_score = sum(
            count for kw, count in top_keywords
            if kw in [k.lower() for k in keywords]
        )

        question_analysis.append({
            'question': q,
            'index': i,
            'keywords': keywords,
            'topic': topic,
            'topic_score': topic_score,
            'importance_score': importance_score
        })

    # Sort by importance
    question_analysis.sort(key=lambda x: x['importance_score'], reverse=True)

    print("\n" + "=" * 50)
    print("✅ TOPIC ANALYSIS COMPLETE")
    print("=" * 50)

    return {
        'top_keywords': top_keywords,
        'topic_frequency': topic_freq,
        'lda_results': lda_results,
        'question_analysis': question_analysis,
        'total_questions': len(questions),
        'total_papers': total_papers
    }


# Testing
if __name__ == "__main__":
    print("=" * 60)
    print("TOPIC ANALYSIS MODULE - TEST")
    print("=" * 60)

    test_questions = [
        "Explain the OSI model and its layers.",
        "What is TCP/IP protocol suite?",
        "Define SQL and its types.",
        "Explain normalization in database.",
        "What is machine learning?",
        "Describe neural network architecture.",
        "Explain inheritance in OOP.",
        "What is polymorphism?",
        "Define process scheduling in OS.",
        "Explain deadlock prevention.",
    ]

    results = comprehensive_topic_analysis(test_questions, total_papers=2)

    print("\n\nTop Keywords:")
    for kw, count in results['top_keywords'][:10]:
        print(f"  {kw}: {count}")

    print("\n\nTopic Distribution:")
    for topic, count in results['topic_frequency']['top_topics']:
        print(f"  {topic}: {count} questions")

