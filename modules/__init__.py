# This file makes the modules folder a proper Python package
# This allows imports like: from modules.preprocessing import preprocess_text, analyze_topics

# Core preprocessing
from .preprocessing import preprocess_text, extract_questions, analyze_text, analyze_topics

# Text cleaning (NEW)
from .text_cleaner import clean_question_text, is_valid_question, clean_instruction_noise

# Advanced Question Extractor (filters out instructions)
from .question_extractor import extract_questions_advanced, filter_questions_list, is_instruction_line

# Semantic similarity (NEW)
from .similarity import group_similar_questions, find_repeated_questions, classify_importance

# Topic analysis (NEW)
from .topic_analysis import comprehensive_topic_analysis, extract_global_keywords

# Question ranking (NEW)
from .question_ranker import rank_questions, get_important_questions_report

# Paper generation
from .generator import generate_predicted_paper
from .practice_paper_generator import generate_practice_paper

# PDF export
from .pdf_generator import create_pdf, create_important_questions_pdf

__all__ = [
    # Core
    'preprocess_text', 'extract_questions', 'analyze_text', 'analyze_topics',
    # Text cleaning
    'clean_question_text', 'is_valid_question', 'clean_instruction_noise',
    # Question extraction
    'extract_questions_advanced', 'filter_questions_list', 'is_instruction_line',
    # Similarity
    'group_similar_questions', 'find_repeated_questions', 'classify_importance',
    # Topic analysis
    'comprehensive_topic_analysis', 'extract_global_keywords',
    # Ranking
    'rank_questions', 'get_important_questions_report',
    # Paper generation
    'generate_predicted_paper', 'generate_practice_paper',
    # PDF
    'create_pdf', 'create_important_questions_pdf'
]
