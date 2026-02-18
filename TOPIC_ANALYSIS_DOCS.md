# 📊 Topic Analysis Module - Complete Documentation

## Overview
The **Topic Analysis Module** (`analyze_topics` function) is an advanced NLP feature for the PrepVision AI Question Paper Predictor. It automatically identifies important topics and ranks questions by their importance based on keyword frequency analysis.

---

## ✅ What Was Created

### 1. New Function: `analyze_topics(tokens, questions)`

**Location:** `modules/preprocessing.py`

**Purpose:**
- Performs word frequency analysis
- Identifies most important topics/keywords
- Ranks questions by importance score
- Helps students prioritize their study focus

---

## 📋 Requirements Satisfied

| Requirement | Status | Implementation |
|------------|--------|----------------|
| 1. Create `analyze_topics(tokens, questions)` | ✅ | Lines 187-286 in preprocessing.py |
| 2. Word frequency analysis using Counter | ✅ | Uses `collections.Counter` |
| 3. Remove short words (length < 3) | ✅ | Filters tokens before analysis |
| 4. Identify most common keywords | ✅ | Returns top 10 keywords with frequencies |
| 5. Importance scoring for questions | ✅ | Scores based on keyword frequency |
| 6. Return top_keywords | ✅ | List of (word, frequency) tuples |
| 7. Return ranked_questions | ✅ | Sorted by importance score |
| 8. Simple, readable code | ✅ | Well-commented, student-friendly |

---

## 🎯 Function Signature

```python
def analyze_topics(tokens, questions):
    """
    Analyze topics from tokens and rank questions by importance.
    
    Args:
        tokens (list): List of preprocessed tokens from preprocess_text()
        questions (list): List of questions from extract_questions()
    
    Returns:
        dict: {
            'top_keywords': [(word, frequency), ...],  # Top 10 most common words
            'ranked_questions': [(question, score, index), ...],  # Sorted by score
            'keyword_count': int,  # Total unique keywords
            'avg_score': float  # Average importance score
        }
    """
```

---

## 🔍 How It Works

### Step 1: Filter Short Words
```python
# Remove words with length < 3
filtered_tokens = [word for word in tokens if len(word) >= 3]
```
**Why?** Short words like "is", "of", "it" don't carry meaningful topic information.

### Step 2: Word Frequency Analysis
```python
from collections import Counter
word_freq = Counter(filtered_tokens)
```
**Result:** Counts how many times each word appears in the document.

### Step 3: Identify Top Keywords
```python
top_keywords = word_freq.most_common(10)  # Top 10
```
**Output:** `[('database', 15), ('explain', 4), ('data', 4), ...]`

### Step 4: Score Questions
For each question:
1. Convert to lowercase and clean
2. Split into words
3. Count how many top keywords it contains
4. Add bonus points based on overall word frequency
5. Store as `(question, score, original_index)`

### Step 5: Rank by Score
```python
ranked_questions = sorted(question_scores, key=lambda x: x[1], reverse=True)
```
**Result:** Questions sorted from most to least important.

---

## 💻 Usage Examples

### Basic Usage

```python
from modules.preprocessing import preprocess_text, extract_questions, analyze_topics

# Your question paper text
text = """
Q1. Define database management system.
Q2. Explain normalization in database design.
...
"""

# Step 1: Preprocess
cleaned_text, tokens = preprocess_text(text)

# Step 2: Extract questions
questions = extract_questions(text)

# Step 3: Analyze topics
analysis = analyze_topics(tokens, questions)

# Access results
print("Top Keywords:", analysis['top_keywords'])
print("Ranked Questions:", analysis['ranked_questions'])
```

### Advanced Usage with Flask App

```python
# In app.py after OCR extraction:

@app.route('/upload', methods=['POST'])
def upload_file():
    # ... OCR extraction code ...
    
    # NLP Processing
    cleaned_text, tokens = preprocess_text(extracted_text)
    questions = extract_questions(extracted_text)
    
    # Topic Analysis (NEW)
    topic_analysis = analyze_topics(tokens, questions)
    
    # Pass to template
    return render_template('result.html',
                         extracted_text=extracted_text,
                         cleaned_text=cleaned_text,
                         questions=questions,
                         top_keywords=topic_analysis['top_keywords'],
                         ranked_questions=topic_analysis['ranked_questions'],
                         avg_score=topic_analysis['avg_score'])
```

---

## 📊 Sample Output

### Input:
```
Q1. Define database management system and explain its advantages.
Q2. What are the different types of database models?
Q3. Explain normalization in database design.
...
```

### Output:
```python
{
    'top_keywords': [
        ('database', 15),
        ('explain', 4),
        ('data', 4),
        ('sql', 4),
        ('key', 4),
        ...
    ],
    'ranked_questions': [
        ('Define database management system...', 11.10, 1),
        ('What is SQL? Write queries...', 9.00, 4),
        ('Explain normalization in database...', 8.90, 3),
        ...
    ],
    'keyword_count': 66,
    'avg_score': 7.81
}
```

---

## 🎨 Visualization Ideas

### 1. Keyword Cloud Display
```html
<!-- Display top keywords with size based on frequency -->
{% for word, freq in top_keywords %}
    <span style="font-size: {{ freq * 2 }}px">{{ word }}</span>
{% endfor %}
```

### 2. Question Priority Badges
```html
<!-- Color-code questions by importance -->
{% for question, score, idx in ranked_questions %}
    {% if score >= avg_score * 1.5 %}
        <div class="badge-high">HIGH PRIORITY</div>
    {% elif score >= avg_score %}
        <div class="badge-medium">MEDIUM</div>
    {% else %}
        <div class="badge-low">LOW</div>
    {% endif %}
    {{ question }}
{% endfor %}
```

### 3. Progress Bar for Scores
```html
{% for question, score, idx in ranked_questions %}
    <div class="progress">
        <div class="bar" style="width: {{ (score / max_score * 100) }}%"></div>
    </div>
{% endfor %}
```

---

## 🧪 Testing

### Run Module Tests
```bash
python modules/preprocessing.py
```

### Run Example Demo
```bash
python example_topic_analysis.py
```

**Expected Output:**
- ✅ Top 10 keywords with frequencies
- ✅ Ranked questions with scores
- ✅ Statistics (total keywords, average score)
- ✅ Detailed breakdown of top question

---

## 🔧 Scoring Algorithm

### Basic Score Calculation:
```
For each question:
    score = 0
    
    # Count top keyword matches
    for each word in question:
        if word in top_10_keywords:
            score += 1
    
    # Add frequency bonus
    for each word in question (length >= 3):
        if word in word_frequency_map:
            score += word_frequency[word] * 0.1
    
    final_score = score
```

### Example:
```
Question: "Define database management system"
Top Keywords: ['database', 'management', 'define', ...]

Scoring:
- 'database' in top keywords → +1
- 'management' in top keywords → +1  
- 'define' in top keywords → +1
- 'database' appears 15 times → +1.5 (15 * 0.1)
- 'management' appears 2 times → +0.2 (2 * 0.1)

Total Score: 4.7
```

---

## 📈 Integration with Flask App

### Recommended Flow:
```
1. User uploads PDF/Image
         ↓
2. OCR extracts text
         ↓
3. preprocess_text() → tokens
         ↓
4. extract_questions() → questions
         ↓
5. analyze_topics() → keywords + rankings
         ↓
6. Display all results in result.html
```

---

## 🎓 Student-Friendly Features

1. **Simple Logic**: Uses basic counting and sorting
2. **Clear Comments**: Every step explained
3. **Visual Output**: Progress bars and badges
4. **Helpful Insights**: Shows why questions are important
5. **Error Handling**: Graceful fallbacks for edge cases

---

## 🚀 Future Enhancements

### Potential Additions:
- [ ] TF-IDF scoring instead of simple frequency
- [ ] Topic clustering (group related questions)
- [ ] Difficulty estimation
- [ ] Subject/chapter classification
- [ ] Trend analysis across multiple papers
- [ ] Exam prediction based on historical patterns

---

## 📝 Files Modified/Created

| File | Action | Description |
|------|--------|-------------|
| `modules/preprocessing.py` | Modified | Added `analyze_topics()` function |
| `example_topic_analysis.py` | Created | Demonstration script |
| `TOPIC_ANALYSIS_DOCS.md` | Created | This documentation |

---

## ✅ Verification Checklist

- [x] Function `analyze_topics()` created
- [x] Uses `collections.Counter` for frequency analysis
- [x] Filters words with length < 3
- [x] Returns top_keywords as list of tuples
- [x] Returns ranked_questions sorted by score
- [x] Code is well-commented
- [x] Student-friendly and readable
- [x] Tested with sample data
- [x] Example script created
- [x] Documentation complete

---

## 🎯 Summary

The Topic Analysis Module is now **fully implemented** and ready to use. It provides:

✅ **Word frequency analysis** using `Counter`  
✅ **Top keyword identification** (top 10 most common)  
✅ **Question importance ranking** (scored and sorted)  
✅ **Clean, beginner-friendly code** with comments  
✅ **Complete example** with database questions  
✅ **Comprehensive documentation**

**Status:** ✅ All requirements satisfied and tested successfully!

---

*Documentation created: February 18, 2026*  
*Module version: 1.0*  
*Part of PrepVision AI - Question Paper Predictor*

