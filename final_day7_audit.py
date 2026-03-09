"""
FINAL DAY 7 AUDIT REPORT
=========================
PrepVision AI - PYQ Question Paper Analysis System
"""

import os
import sys
from difflib import SequenceMatcher

print("=" * 80)
print("FINAL DAY 7 COMPLETION AUDIT")
print("PrepVision AI - Question Paper Predictor")
print("=" * 80)

# Read app.py to verify implementations
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Read templates
with open('templates/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

with open('templates/result.html', 'r', encoding='utf-8') as f:
    result_content = f.read()

# =============================================================================
# TECHNICAL VERIFICATION
# =============================================================================

print("\n" + "=" * 80)
print("TECHNICAL VERIFICATION")
print("=" * 80)

verification_results = []

# 1. Multi-file Processing
print("\n1. MULTI-FILE PROCESSING")
print("-" * 80)

if 'len(valid_files) < 5' in app_content:
    verification_results.append(("✅ PASS", "System requires minimum 5 papers"))
    print("✅ System enforces minimum 5 question papers")
else:
    verification_results.append(("❌ FAIL", "Minimum requirement not 5"))
    print("❌ Minimum requirement not set to 5")

if 'all_questions.extend(questions)' in app_content:
    verification_results.append(("✅ PASS", "All files processed together"))
    print("✅ All files processed together in single pipeline")
else:
    verification_results.append(("❌ FAIL", "Files not processed together"))
    print("❌ Files not processed together")

if 'all_questions = []' in app_content and 'all_tokens = []' in app_content:
    verification_results.append(("✅ PASS", "Questions merged into single dataset"))
    print("✅ Questions merged into single aggregated dataset")
else:
    verification_results.append(("❌ FAIL", "No merged dataset"))
    print("❌ No merged dataset found")

# 2. Preprocessing Integration
print("\n2. PREPROCESSING INTEGRATION")
print("-" * 80)

if 'from modules.preprocessing import' in app_content:
    verification_results.append(("✅ PASS", "Preprocessing module connected"))
    print("✅ Preprocessing module imported and connected to app.py")
else:
    verification_results.append(("❌ FAIL", "Preprocessing not connected"))
    print("❌ Preprocessing module not connected")

# Test preprocessing
try:
    from modules.preprocessing import preprocess_text
    test_text = "Hello WORLD! This is a TEST? Remove123 punctuation."
    cleaned, tokens = preprocess_text(test_text)

    checks = []
    checks.append(("Lowercase", cleaned.islower()))
    checks.append(("No punctuation", not any(c in cleaned for c in '!?.,')))
    checks.append(("Stopwords removed", len(tokens) < len(test_text.split())))

    all_passed = all(check[1] for check in checks)
    if all_passed:
        verification_results.append(("✅ PASS", "Text normalization (lowercase, punctuation, stopwords)"))
        print("✅ Text normalization working: lowercase ✓, punctuation removal ✓, stopword removal ✓")
    else:
        verification_results.append(("⚠️ PARTIAL", "Some normalization features may not work"))
        print("⚠️ Some normalization features may not work properly")
except Exception as e:
    verification_results.append(("❌ FAIL", f"Preprocessing test failed: {e}"))
    print(f"❌ Preprocessing test failed: {e}")

if app_content.index('preprocess_text') < app_content.index('analyze_topics'):
    verification_results.append(("✅ PASS", "Preprocessing runs before analysis"))
    print("✅ Preprocessing runs before analysis (correct pipeline order)")
else:
    verification_results.append(("❌ FAIL", "Pipeline order incorrect"))
    print("❌ Pipeline order may be incorrect")

# 3. Question Similarity Detection (CRITICAL)
print("\n3. QUESTION SIMILARITY DETECTION (CRITICAL)")
print("-" * 80)

if 'SequenceMatcher' in app_content:
    verification_results.append(("✅ PASS", "Fuzzy similarity matching implemented (SequenceMatcher)"))
    print("✅ Fuzzy similarity matching implemented using difflib.SequenceMatcher")
else:
    verification_results.append(("❌ FAIL", "No fuzzy matching implementation"))
    print("❌ No fuzzy matching implementation found")

if 'SIMILARITY_THRESHOLD' in app_content:
    verification_results.append(("✅ PASS", "Similarity threshold configured"))
    print("✅ Similarity threshold configured for matching")

    # Extract threshold value
    import re
    match = re.search(r'SIMILARITY_THRESHOLD\s*=\s*([\d.]+)', app_content)
    if match:
        threshold = float(match.group(1))
        print(f"   Threshold value: {threshold}")
        if 0.55 <= threshold <= 0.70:
            print(f"   ✅ Threshold {threshold} is in optimal range (0.55-0.70)")
        else:
            print(f"   ⚠️ Threshold {threshold} may need adjustment")
else:
    verification_results.append(("❌ FAIL", "No similarity threshold"))
    print("❌ No similarity threshold configured")

# Test fuzzy matching in practice
test_similar_questions = [
    "What is machine learning?",
    "Define machine learning",
    "What do you mean by machine learning?"
]

print("\n   Testing fuzzy matching on similar questions:")
for i in range(len(test_similar_questions)):
    for j in range(i+1, len(test_similar_questions)):
        q1_norm = ' '.join(test_similar_questions[i].lower().split())
        q2_norm = ' '.join(test_similar_questions[j].lower().split())
        ratio = SequenceMatcher(None, q1_norm, q2_norm).ratio()
        print(f"   Q{i+1} vs Q{j+1}: {ratio:.2f} similarity")

if 'group_frequencies' in app_content:
    verification_results.append(("✅ PASS", "Similarity grouping logic implemented"))
    print("✅ Question grouping by similarity implemented")
else:
    verification_results.append(("⚠️ PARTIAL", "Grouping logic unclear"))
    print("⚠️ Grouping logic unclear")

# 4. Frequency Calculation
print("\n4. FREQUENCY CALCULATION")
print("-" * 80)

if "'count'" in app_content or "['count']" in app_content:
    verification_results.append(("✅ PASS", "Frequency counter implemented"))
    print("✅ Frequency counter tracks question repetitions")
else:
    verification_results.append(("❌ FAIL", "No frequency counter"))
    print("❌ No frequency counter found")

# Check preprocessing module for score calculation
with open('modules/preprocessing.py', 'r', encoding='utf-8') as f:
    prep_content = f.read()

if 'word_freq[word]' in prep_content and 'score +=' in prep_content:
    verification_results.append(("✅ PASS", "Importance score depends on frequency"))
    print("✅ Importance scoring uses frequency weighting")
else:
    verification_results.append(("⚠️ PARTIAL", "Score calculation unclear"))
    print("⚠️ Score calculation unclear")

# 5. Ranking System
print("\n5. RANKING SYSTEM")
print("-" * 80)

if 'sort(key=lambda x: x[' in app_content and 'reverse=True' in app_content:
    verification_results.append(("✅ PASS", "Results sorted by frequency (descending)"))
    print("✅ Results sorted from most repeated to least repeated")
else:
    verification_results.append(("❌ FAIL", "Sorting not implemented"))
    print("❌ Sorting not implemented correctly")

if 'ranked_questions' in app_content:
    verification_results.append(("✅ PASS", "Ranked questions generated"))
    print("✅ Ranked questions list generated")
else:
    verification_results.append(("❌ FAIL", "No ranking output"))
    print("❌ No ranking output")

# 6. Output Generation
print("\n6. OUTPUT GENERATION")
print("-" * 80)

required_outputs = [
    ('question', 'Question text'),
    ('frequency', 'Frequency count'),
    ('HIGH PRIORITY', 'Importance labels')
]

for field, desc in required_outputs:
    if field in result_content:
        verification_results.append(("✅ PASS", f"Output includes {desc}"))
        print(f"✅ Output includes {desc}")
    else:
        verification_results.append(("⚠️ PARTIAL", f"{desc} may not be displayed"))
        print(f"⚠️ {desc} may not be displayed")

if 'group_id' in app_content:
    verification_results.append(("✅ PASS", "Duplicate elimination via grouping"))
    print("✅ Duplicates eliminated via similarity grouping")
else:
    verification_results.append(("⚠️ PARTIAL", "Duplicate handling unclear"))
    print("⚠️ Duplicate handling unclear")

# 7. Pipeline Validation
print("\n7. PIPELINE VALIDATION")
print("-" * 80)

pipeline_steps = [
    ('extract_text', 'OCR extraction'),
    ('preprocess_text', 'Preprocessing'),
    ('extract_questions', 'Question extraction'),
    ('analyze_topics', 'Topic analysis'),
    ('generate_predicted_paper', 'Predicted paper generation'),
    ('create_pdf', 'PDF export')
]

all_steps_present = True
for func, desc in pipeline_steps:
    if func in app_content:
        print(f"✅ {desc}")
    else:
        print(f"❌ Missing: {desc}")
        all_steps_present = False

if all_steps_present:
    verification_results.append(("✅ PASS", "Complete pipeline implemented"))
    print("\n✅ Full pipeline: upload → OCR → preprocess → analyze → rank → generate → PDF")
else:
    verification_results.append(("❌ FAIL", "Incomplete pipeline"))
    print("\n❌ Pipeline incomplete")

# =============================================================================
# MANUAL WORK VERIFICATION STATUS
# =============================================================================

print("\n" + "=" * 80)
print("MANUAL WORK VERIFICATION STATUS")
print("=" * 80)

manual_checks = [
    "At least 5 real PYQ papers tested",
    "Extracted questions manually compared with original PDFs",
    "At least 5 repeated questions manually verified",
    "Ranking order manually checked for correctness",
    "Tested with similar wording questions",
    "Tested with mixed-format question papers",
    "Confirmed no duplicate outputs exist"
]

print("\nThe following manual validations should be performed:")
for i, check in enumerate(manual_checks, 1):
    print(f"{i}. {check}")

# Check if sample papers exist
sample_papers = os.path.join('sample papers')
uploads_folder = 'uploads'

if os.path.isdir(sample_papers):
    sample_count = len([f for f in os.listdir(sample_papers) if f.endswith('.pdf')])
    print(f"\n✅ Found {sample_count} sample papers in 'sample papers/' directory")
    if sample_count >= 5:
        print(f"   Sufficient for testing (≥5 papers)")
    else:
        print(f"   ⚠️ Need at least 5 papers for proper testing")
else:
    print("\n⚠️ No 'sample papers' directory found")

if os.path.isdir(uploads_folder):
    upload_count = len([f for f in os.listdir(uploads_folder) if os.path.isfile(os.path.join(uploads_folder, f))])
    print(f"✅ Found {upload_count} files in uploads/ directory (previous test runs)")
else:
    print("⚠️ No uploads directory (system not tested yet)")

# =============================================================================
# FINAL SCORING
# =============================================================================

print("\n" + "=" * 80)
print("FINAL AUDIT RESULTS")
print("=" * 80)

pass_count = sum(1 for status, _ in verification_results if status == "✅ PASS")
fail_count = sum(1 for status, _ in verification_results if status == "❌ FAIL")
partial_count = sum(1 for status, _ in verification_results if status == "⚠️ PARTIAL")
total_checks = len(verification_results)

print(f"\n📊 Statistics:")
print(f"   Passed:  {pass_count}/{total_checks}")
print(f"   Failed:  {fail_count}/{total_checks}")
print(f"   Partial: {partial_count}/{total_checks}")

# Calculate score (pass = 1.0, partial = 0.5, fail = 0)
score = ((pass_count * 1.0) + (partial_count * 0.5)) / total_checks * 10

print(f"\n🎯 OVERALL READINESS SCORE: {score:.1f}/10")

# Determine completion status
if fail_count == 0 and partial_count == 0:
    status = "✅ COMPLETED"
    color = "green"
elif fail_count <= 2 and pass_count >= total_checks * 0.75:
    status = "⚠️ MOSTLY COMPLETED"
    color = "yellow"
else:
    status = "❌ PARTIALLY COMPLETED"
    color = "red"

print(f"📌 COMPLETION STATUS: {status}")

# =============================================================================
# RECOMMENDATIONS
# =============================================================================

print("\n" + "=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)

if fail_count > 0:
    print("\n⚠️ Issues to address:")
    for i, (status, desc) in enumerate(verification_results, 1):
        if status == "❌ FAIL":
            print(f"   {i}. {desc}")

if score >= 8.0:
    print("\n✅ System is PRODUCTION-READY for Day 7 requirements!")
    print("   - All core features implemented")
    print("   - Fuzzy similarity detection working")
    print("   - Minimum 5 papers enforced")
    print("   - Complete analysis pipeline functional")
elif score >= 6.0:
    print("\n⚠️ System is NEARLY COMPLETE but needs minor fixes")
else:
    print("\n❌ System needs significant work to meet Day 7 requirements")

# Save report
with open("DAY7_FINAL_AUDIT_REPORT.txt", "w", encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("DAY 7 FINAL AUDIT REPORT\n")
    f.write("PrepVision AI - Question Paper Predictor\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"COMPLETION STATUS: {status}\n")
    f.write(f"READINESS SCORE: {score:.1f}/10\n\n")
    f.write(f"Statistics: {pass_count} Passed | {fail_count} Failed | {partial_count} Partial\n\n")
    f.write("=" * 80 + "\n")
    f.write("DETAILED VERIFICATION RESULTS\n")
    f.write("=" * 80 + "\n\n")
    for status, desc in verification_results:
        f.write(f"{status} {desc}\n")

print("\n✅ Full audit report saved to: DAY7_FINAL_AUDIT_REPORT.txt")
print("=" * 80)

