# This file makes the modules folder a proper Python package
# This allows imports like: from modules.preprocessing import preprocess_text, analyze_topics

from .preprocessing import preprocess_text, extract_questions, analyze_text, analyze_topics
from .generator import generate_predicted_paper

__all__ = ['preprocess_text', 'extract_questions', 'analyze_text', 'analyze_topics', 'generate_predicted_paper']
