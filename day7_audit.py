"""
DAY 7 COMPREHENSIVE AUDIT - PrepVision AI
==========================================
Testing all Day 7 requirements with real-world scenarios
"""

import os
import sys
from collections import Counter
from difflib import SequenceMatcher

print("=" * 80)
print("DAY 7 AUDIT - PrepVision AI Question Paper Analysis")
print("=" * 80)

# =============================================================================
# TECHNICAL VERIFICATION CHECKS
# =============================================================================

results = []
critical_issues = []
warnings = []

print("\n" + "=" * 80)
print("1. MULTI-FILE PROCESSING")
print("=" * 80)

# Check 1.1: Minimum file requirement
try:
    # Read app.py to check minimum requirement
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'at least 2' in content:
            min_files = 2
            if min_files < 5:
                critical_issues.append("System requires minimum 2 files, but Day 7 requires MINIMUM 5 files")
                results.append("❌ FAIL: Minimum file requirement is 2, not 5 (Day 7 requirement)")
            else:
                results.append("✅ PASS: Minimum file requirement meets Day 7 standard")
        else:
            results.append("⚠️ WARNING: Could not verify minimum file requirement")
except Exception as e:
    results.append(f"❌ ERROR: {e}")

# Check 1.2: Files processed together
if 'all_questions.extend(questions)' in content and 'all_tokens.extend(tokens)' in content:
    results.append("✅ PASS: All files are processed together (merged dataset)")
else:
    results.append("❌ FAIL: Files may not be processed together properly")

# Check 1.3: Single merged dataset
if 'all_questions = []' in content and 'all_tokens = []' in content:
    results.append("✅ PASS: Questions merged into single dataset")
else:
    results.append("❌ FAIL: No evidence of merged dataset")

print("\n" + "=" * 80)
print("2. PREPROCESSING INTEGRATION")
print("=" * 80)

# Check 2.1: Preprocessing module connected
if 'from modules.preprocessing import' in content:
    results.append("✅ PASS: Preprocessing module imported in app.py")
else:
    results.append("❌ FAIL: Preprocessing module not imported")

# Check 2.2: Text normalization verification
try:
    from modules.preprocessing import preprocess_text
    test_text = "HELLO World! This IS a TEST? 123"
    cleaned, tokens = preprocess_text(test_text)

    # Check lowercase
    if cleaned.islower():
        results.append("✅ PASS: Text normalization - lowercase conversion")
    else:
        results.append("❌ FAIL: Text not converted to lowercase")

    # Check punctuation removal (no punctuation should remain)
    if not any(char in cleaned for char in '!?.,"\''):
        results.append("✅ PASS: Text normalization - punctuation removal")
    else:
        results.append("⚠️ WARNING: Some punctuation may remain")

    # Check stopword removal (basic check)
    if len(tokens) < len(test_text.split()):
        results.append("✅ PASS: Text normalization - stopword removal active")
    else:
        results.append("⚠️ WARNING: Stopword removal may not be working")

except Exception as e:
    results.append(f"❌ ERROR: Preprocessing test failed - {e}")

# Check 2.3: Preprocessing runs before analysis
if 'preprocess_text(extracted_text)' in content and content.index('preprocess_text') < content.index('analyze_topics'):
    results.append("✅ PASS: Preprocessing runs before analysis")
else:
    results.append("⚠️ WARNING: Preprocessing order unclear")

print("\n" + "=" * 80)
print("3. QUESTION SIMILARITY DETECTION (CRITICAL)")
print("=" * 80)

# Check 3.1: Different wording detection
# This is the MOST CRITICAL check for Day 7
test_questions = [
    "What is machine learning?",
    "Define machine learning and its applications",
    "Explain the concept of machine learning",
    "What do you mean by machine learning?",
    "Write a short note on machine learning"
]

# Check current normalization approach
normalized_set = set()
for q in test_questions:
    normalized = ' '.join(q.lower().split())
    normalized_set.add(normalized)

if len(normalized_set) == len(test_questions):
    critical_issues.append("CRITICAL: Similar questions with DIFFERENT WORDING are NOT detected as similar")
    results.append("❌ FAIL: Question similarity detection - Only exact matches detected")
    results.append("   Current system: Normalizes and checks exact match only")
    results.append("   Day 7 Requirement: Should detect 'What is ML?' and 'Define ML' as similar")

    # Test if any fuzzy matching exists
    if 'difflib' in content or 'SequenceMatcher' in content or 'similarity' in content.lower():
        results.append("   ℹ️ Found fuzzy matching code, but may not be used correctly")
    else:
        results.append("   ❌ No fuzzy/semantic similarity detection implemented")
        critical_issues.append("Missing implementation: Fuzzy string matching (difflib, SequenceMatcher, or embeddings)")
else:
    results.append("✅ PASS: Question similarity detection working")

# Check 3.2: Similarity logic implementation
if 'normalized_questions' in content:
    results.append("✅ PASS: Question normalization logic exists")
    if 'SequenceMatcher' in content or 'fuzz' in content or 'cosine' in content:
        results.append("✅ PASS: Advanced similarity method detected")
    else:
        results.append("⚠️ WARNING: Only basic normalization (exact match), no fuzzy matching")
        warnings.append("Implement fuzzy matching using difflib.SequenceMatcher (threshold ~0.75)")
else:
    results.append("❌ FAIL: No similarity logic found")

print("\n" + "=" * 80)
print("4. FREQUENCY CALCULATION")
print("=" * 80)

# Check 4.1: Repetition count
if "'count': 0" in content and "['count'] += 1" in content:
    results.append("✅ PASS: Frequency counter implemented")
else:
    results.append("❌ FAIL: Frequency counter not found")

# Check 4.2: Importance score based on frequency
try:
    from modules.preprocessing import analyze_topics

    # Read analyze_topics implementation
    with open('modules/preprocessing.py', 'r', encoding='utf-8') as f:
        prep_content = f.read()

    if 'word_freq[word]' in prep_content and 'score +=' in prep_content:
        results.append("✅ PASS: Importance score depends on frequency")
    else:
        results.append("⚠️ WARNING: Importance scoring may not use frequency")

except Exception as e:
    results.append(f"❌ ERROR: Could not verify importance scoring - {e}")

print("\n" + "=" * 80)
print("5. RANKING SYSTEM")
print("=" * 80)

# Check 5.1: Sorting by frequency
if 'sort(key=lambda x: x[' in content and 'reverse=True' in content:
    results.append("✅ PASS: Results sorted in descending order")
else:
    results.append("❌ FAIL: Sorting not implemented correctly")

# Check 5.2: Ranked questions verification
if 'ranked_questions' in content:
    results.append("✅ PASS: Ranked questions variable exists")
else:
    results.append("❌ FAIL: No ranked questions found")

print("\n" + "=" * 80)
print("6. OUTPUT GENERATION")
print("=" * 80)

# Check 6.1: Output includes required fields
required_fields = ['question', 'frequency']
fields_found = all(field in content for field in required_fields)

if fields_found:
    results.append("✅ PASS: Output includes question text and frequency")
else:
    results.append("❌ FAIL: Missing required output fields")

# Check 6.2: Importance labels
# Check result.html for importance labels
try:
    with open('templates/result.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    if 'HIGH PRIORITY' in html_content or 'MEDIUM' in html_content or 'LOW' in html_content:
        results.append("✅ PASS: Importance labels displayed (High/Medium/Low)")
    else:
        results.append("⚠️ WARNING: Importance labels may not be displayed")

except Exception as e:
    results.append(f"⚠️ WARNING: Could not verify HTML output - {e}")

# Check 6.3: No duplicates in output
if 'normalized_questions' in content and 'if normalized not in normalized_questions' in content:
    results.append("✅ PASS: Duplicate detection implemented")
else:
    results.append("❌ FAIL: No duplicate detection found")

print("\n" + "=" * 80)
print("7. PIPELINE VALIDATION")
print("=" * 80)

# Check 7.1: Full pipeline flow
pipeline_steps = [
    ('extract_text', 'OCR extraction'),
    ('preprocess_text', 'Preprocessing'),
    ('extract_questions', 'Question extraction'),
    ('analyze_topics', 'Topic analysis'),
    ('generate_predicted_paper', 'Predicted paper generation')
]

for func, desc in pipeline_steps:
    if func in content:
        results.append(f"✅ PASS: Pipeline step - {desc}")
    else:
        results.append(f"❌ FAIL: Missing pipeline step - {desc}")

# Check 7.2: Module connections
if all(step[0] in content for step in pipeline_steps):
    results.append("✅ PASS: All modules actively connected")
else:
    results.append("❌ FAIL: Some modules not connected to pipeline")

print("\n" + "=" * 80)
print("8. PDF EXPORT (DAY 6 COMPLETION)")
print("=" * 80)

# Check 8.1: PDF module exists and imported
if 'from modules.pdf_generator import create_pdf' in content:
    results.append("✅ PASS: PDF generator imported")
else:
    results.append("❌ FAIL: PDF generator not imported")

# Check 8.2: PDF generation called
if 'create_pdf(predicted_paper)' in content:
    results.append("✅ PASS: PDF generation integrated into pipeline")
else:
    results.append("❌ FAIL: PDF generation not called")

# Check 8.3: Download route
if '@app.route(\'/download\')' in content:
    results.append("✅ PASS: PDF download route implemented")
else:
    results.append("❌ FAIL: No download route found")

# =============================================================================
# SUMMARY AND SCORING
# =============================================================================

print("\n\n" + "=" * 80)
print("AUDIT RESULTS SUMMARY")
print("=" * 80)

pass_count = sum(1 for r in results if '✅ PASS' in r)
fail_count = sum(1 for r in results if '❌ FAIL' in r)
warning_count = sum(1 for r in results if '⚠️ WARNING' in r)

for r in results:
    print(r)

print("\n" + "=" * 80)
print(f"STATISTICS: {pass_count} Passed | {fail_count} Failed | {warning_count} Warnings")
print("=" * 80)

# Calculate score
total_checks = len(results)
score = (pass_count / total_checks) * 10 if total_checks > 0 else 0

print(f"\n📊 OVERALL READINESS SCORE: {score:.1f}/10")

# Determine completion status
if len(critical_issues) > 0:
    status = "PARTIALLY COMPLETED"
elif fail_count > 0:
    status = "PARTIALLY COMPLETED"
else:
    status = "COMPLETED"

print(f"🎯 COMPLETION STATUS: {status}")

# Display critical issues
if critical_issues:
    print("\n" + "=" * 80)
    print("⚠️ CRITICAL ISSUES")
    print("=" * 80)
    for i, issue in enumerate(critical_issues, 1):
        print(f"{i}. {issue}")

# Display warnings
if warnings:
    print("\n" + "=" * 80)
    print("⚠️ WARNINGS")
    print("=" * 80)
    for i, warning in enumerate(warnings, 1):
        print(f"{i}. {warning}")

# Write full report to file
with open("DAY7_AUDIT_COMPLETE_REPORT.txt", "w", encoding='utf-8') as f:
    f.write("DAY 7 COMPREHENSIVE AUDIT REPORT\n")
    f.write("=" * 80 + "\n\n")
    f.write("PROJECT: PrepVision AI - PYQ Question Analysis\n")
    f.write(f"COMPLETION STATUS: {status}\n")
    f.write(f"READINESS SCORE: {score:.1f}/10\n\n")
    f.write("=" * 80 + "\n")
    f.write("DETAILED RESULTS\n")
    f.write("=" * 80 + "\n\n")
    for r in results:
        f.write(r + "\n")
    f.write("\n" + "=" * 80 + "\n")
    f.write(f"STATISTICS: {pass_count} Passed | {fail_count} Failed | {warning_count} Warnings\n")
    f.write("=" * 80 + "\n\n")
    if critical_issues:
        f.write("CRITICAL ISSUES:\n")
        for i, issue in enumerate(critical_issues, 1):
            f.write(f"{i}. {issue}\n")
    if warnings:
        f.write("\nWARNINGS:\n")
        for i, warning in enumerate(warnings, 1):
            f.write(f"{i}. {warning}\n")

print("\n✅ Full report saved to: DAY7_AUDIT_COMPLETE_REPORT.txt")
print("=" * 80)

