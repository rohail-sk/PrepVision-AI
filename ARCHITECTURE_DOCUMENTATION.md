# PrepVision AI — System Architecture Documentation

## Overview

PrepVision AI is an intelligent exam preparation tool that analyzes Previous Year Question (PYQ) papers to help students identify important questions and topics for exam preparation.

## Key Features

### 1. Important Question Analyzer
Identifies and ranks questions based on:
- Frequency of appearance across papers
- Topic relevance and keyword density
- Semantic similarity grouping

### 2. Practice Paper Generator
Creates a practice question paper organized into sections (A, B, C) based on question importance and frequency analysis.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                     (templates/index.html)                      │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FILE UPLOAD                             │
│                    (app.py - upload_file)                       │
│              Accepts: PDF, JPG, JPEG, PNG (≥2 files)            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TEXT EXTRACTION                            │
│                    (app.py - extract_text)                      │
│              OCR: pytesseract | PDF: pdfplumber                 │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TEXT CLEANING                              │
│                 (modules/text_cleaner.py)                       │
│    • Remove instruction phrases (Attempt any, Marks, P.T.O)     │
│    • Clean question numbers and markers                         │
│    • Validate question content                                  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   QUESTION EXTRACTION                           │
│                (modules/preprocessing.py)                       │
│    • Pattern-based extraction (Q1., 1., Q1))                    │
│    • Tokenization and lemmatization                             │
│    • Stopword removal                                           │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SEMANTIC SIMILARITY                            │
│                  (modules/similarity.py)                        │
│    • TF-IDF vectorization                                       │
│    • Cosine similarity calculation                              │
│    • Question grouping (65% threshold)                          │
│    • Repeated question detection                                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TOPIC ANALYSIS                               │
│                (modules/topic_analysis.py)                      │
│    • Keyword extraction                                         │
│    • Topic categorization                                       │
│    • Frequency analysis                                         │
│    • Optional LDA topic modeling                                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  IMPORTANCE RANKING                             │
│                (modules/question_ranker.py)                     │
│    • Frequency score (40%)                                      │
│    • Topic relevance (30%)                                      │
│    • Keyword density (20%)                                      │
│    • Length factor (10%)                                        │
└─────────────────────────────────────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│  IMPORTANT QUESTIONS     │    │   PRACTICE PAPER         │
│  REPORT                  │    │   GENERATOR              │
│  (question_ranker.py)    │    │   (practice_paper_       │
│                          │    │    generator.py)         │
│  • Highly Important      │    │                          │
│  • Important             │    │  • Section C (Long)      │
│  • Moderately Important  │    │  • Section B (Medium)    │
└──────────────────────────┘    │  • Section A (Short)     │
               │                └──────────────────────────┘
               │                               │
               └───────────────┬───────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       PDF EXPORT                                │
│                  (modules/pdf_generator.py)                     │
│              Professional PDF using ReportLab                   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESULT DISPLAY                             │
│                   (templates/result.html)                       │
│    • Statistics cards                                           │
│    • Repeated questions list                                    │
│    • Important questions report                                 │
│    • Practice paper preview                                     │
│    • PDF download button                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Descriptions

### 1. Text Cleaner (`modules/text_cleaner.py`)
**Purpose:** Remove noise from extracted text

**Functions:**
- `clean_instruction_noise(text)` — Removes exam instructions
- `clean_question_text(question)` — Cleans individual questions
- `is_valid_question(question)` — Validates question content

**Noise Patterns Removed:**
- "Attempt any X questions"
- "Marks: X"
- "P.T.O."
- "Page X"
- Question numbers (Q1., 1., etc.)

### 2. Similarity Module (`modules/similarity.py`)
**Purpose:** Detect semantically similar questions

**Algorithm:** TF-IDF + Cosine Similarity (65% threshold)

**Functions:**
- `normalize_question(question)` — Prepares text for comparison
- `calculate_tfidf_similarity(questions)` — Builds similarity matrix
- `group_similar_questions(questions, threshold)` — Groups similar questions
- `find_repeated_questions(questions, min_occurrences)` — Finds repeats
- `classify_importance(count, total_papers)` — Classifies importance level

**Why TF-IDF is Better:**
- Weights important words higher
- Ignores common/stopwords
- Captures semantic meaning better than character matching

### 3. Topic Analysis (`modules/topic_analysis.py`)
**Purpose:** Analyze question topics and keywords

**Functions:**
- `extract_keywords_from_question(question)` — Gets important keywords
- `identify_question_topic(question)` — Categorizes by topic
- `analyze_topic_frequency(questions)` — Counts topic distribution
- `extract_global_keywords(questions)` — Gets top keywords
- `perform_lda_topic_modeling(questions)` — Optional LDA clustering
- `comprehensive_topic_analysis(questions)` — Full analysis

**Topic Categories:**
- Networking (TCP, IP, OSI, protocols)
- Database (SQL, normalization, DBMS)
- Programming (OOP, functions, arrays)
- Machine Learning (neural networks, classification)
- And more...

### 4. Question Ranker (`modules/question_ranker.py`)
**Purpose:** Rank questions by importance

**Scoring Formula:**
```
Importance Score = Frequency(40%) + Topic(30%) + Keywords(20%) + Length(10%)
```

**Classification Levels:**
| Level | Label | Criteria |
|-------|-------|----------|
| 3 | Highly Important | 4+ occurrences OR score ≥70 |
| 2 | Important | 2-3 occurrences OR score ≥40 |
| 1 | Moderately Important | 1 occurrence |

### 5. Practice Paper Generator (`modules/practice_paper_generator.py`)
**Purpose:** Generate exam-format practice paper

**Section Distribution:**
| Section | Type | Questions | Marks Each |
|---------|------|-----------|------------|
| C | Long Answer | 3 | 10 |
| B | Medium Answer | 5 | 6 |
| A | Short Answer | 5 | 4 |

**Selection Logic:**
- Section C: Top 3 ranked questions (most important)
- Section B: Next 5 ranked questions
- Section A: Next 5 ranked questions

### 6. PDF Generator (`modules/pdf_generator.py`)
**Purpose:** Create downloadable PDF

**Features:**
- Professional formatting
- Color-coded sections
- Generation date
- Instructions included

---

## Data Flow Example

**Input:** 5 PYQ papers uploaded

```
Step 1: OCR/PDF Extraction
        → 120 raw text blocks extracted

Step 2: Question Extraction
        → 95 questions identified

Step 3: Text Cleaning
        → 82 valid questions after cleaning

Step 4: Similarity Grouping (TF-IDF)
        → 45 unique question groups
        → 25 repeated questions detected

Step 5: Topic Analysis
        → Top topics: networking (15), database (12), programming (10)
        → Top keywords: explain, define, describe, protocol, model

Step 6: Importance Ranking
        → 8 Highly Important questions
        → 18 Important questions
        → 19 Moderately Important questions

Step 7: Practice Paper Generation
        → Section C: 3 questions (top ranked)
        → Section B: 5 questions
        → Section A: 5 questions

Step 8: PDF Export
        → File: static/generated/predicted_paper.pdf
```

---

## Improvements Over Previous System

| Aspect | Old System | New System |
|--------|------------|------------|
| Similarity | SequenceMatcher (60%) | TF-IDF + Cosine (65%) |
| Detection | Character-based | Semantic-based |
| Instruction Noise | Not filtered | Comprehensive filtering |
| Topic Analysis | Keyword counting only | Topic categorization + LDA |
| Ranking | Single factor | Multi-factor scoring |
| Output | "Predicted Paper" | "Practice Paper" (accurate) |

---

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Required packages:
# - Flask
# - pytesseract
# - Pillow
# - pdfplumber
# - nltk
# - reportlab
# - scikit-learn (NEW)
```

---

## Usage

1. Upload minimum 2 question papers (PDF/images)
2. System extracts and analyzes questions
3. View important questions report
4. Download practice paper PDF

---

## Technical Notes

### Similarity Threshold
The 65% threshold for TF-IDF similarity was chosen because:
- Lower values (50-60%) create too many false positives
- Higher values (70-80%) miss valid similar questions
- 65% balances precision and recall effectively

### Importance Scoring
The multi-factor scoring provides more accurate rankings than frequency alone:
- **Frequency (40%):** How often the question appears
- **Topic (30%):** How central the topic is to the subject
- **Keywords (20%):** Presence of important subject keywords
- **Length (10%):** Longer questions often require deeper understanding

---

## File Structure

```
PrepVision AI/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── modules/
│   ├── __init__.py                 # Module exports
│   ├── preprocessing.py            # Text preprocessing & question extraction
│   ├── text_cleaner.py             # Instruction noise removal
│   ├── question_extractor.py       # ADVANCED question extraction (filters instructions)
│   ├── similarity.py               # TF-IDF semantic similarity
│   ├── topic_analysis.py           # Topic clustering & keywords
│   ├── question_ranker.py          # Multi-factor importance ranking
│   ├── practice_paper_generator.py # Practice paper generation
│   ├── generator.py                # Legacy paper generator
│   └── pdf_generator.py            # PDF export
├── templates/
│   ├── index.html                  # Upload page
│   └── result.html                 # Results display
├── static/
│   └── generated/                  # Generated PDF storage
└── uploads/                        # Uploaded files storage
```

---

## Academic Description

**PrepVision AI** is an intelligent examination preparation system that employs Natural Language Processing (NLP) techniques to analyze Previous Year Question (PYQ) papers. The system utilizes TF-IDF (Term Frequency-Inverse Document Frequency) vectorization combined with cosine similarity metrics to identify semantically similar questions across multiple examination papers. Through comprehensive frequency analysis and multi-factor importance scoring, the system generates ranked lists of important questions and produces structured practice papers in examination format. This approach significantly reduces manual analysis effort while providing data-driven insights for effective exam preparation.

---

*Document Version: 2.0*
*Last Updated: March 2026*

