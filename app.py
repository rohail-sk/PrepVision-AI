# Import necessary libraries
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import pdfplumber

# Import NLP preprocessing functions
from modules.preprocessing import preprocess_text, extract_questions, analyze_topics

# Import NEW modular components
from modules.text_cleaner import clean_question_text, is_valid_question, clean_instruction_noise
from modules.similarity import group_similar_questions, find_repeated_questions, classify_importance
from modules.topic_analysis import comprehensive_topic_analysis, extract_global_keywords
from modules.question_ranker import rank_questions, get_important_questions_report
from modules.practice_paper_generator import generate_practice_paper

# Import ADVANCED question extractor (filters out instructions)
from modules.question_extractor import extract_questions_advanced, filter_questions_list

# Import question paper generator (legacy support)
from modules.generator import generate_predicted_paper

# Import PDF generator
from modules.pdf_generator import create_pdf, create_important_questions_pdf

# Configure Tesseract path for Windows (uncomment and set path if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Flask app
app = Flask(__name__)

# Secret key for flash messages (change this to a random secret key)
app.secret_key = 'your-secret-key-here-change-in-production'

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Function to check if file extension is allowed
def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    Args:
        filename: Name of the uploaded file
    Returns:
        True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to extract text from uploaded files using OCR
def extract_text(file_path):
    """
    Extract text from images or PDFs using OCR.
    Args:
        file_path: Path to the uploaded file
    Returns:
        Extracted text as string
    Raises:
        Exception: If text extraction fails
    """
    try:
        # Get file extension
        file_extension = file_path.rsplit('.', 1)[1].lower()

        # Process image files (JPG, JPEG, PNG)
        if file_extension in ['jpg', 'jpeg', 'png']:
            # Open image using PIL
            image = Image.open(file_path)

            # Extract text using pytesseract
            text = pytesseract.image_to_string(image)

            return text if text.strip() else "No text found in the image."

        # Process PDF files
        elif file_extension == 'pdf':
            extracted_text = ""

            # Open PDF using pdfplumber
            with pdfplumber.open(file_path) as pdf:
                # Extract text from each page
                for page_num, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text()

                    if page_text:
                        extracted_text += f"--- Page {page_num} ---\n"
                        extracted_text += page_text + "\n\n"

            return extracted_text if extracted_text.strip() else "No text found in the PDF."

        else:
            return "Unsupported file format."

    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")


# Route for homepage
@app.route('/')
def index():
    """
    Render the homepage with file upload form.
    Returns:
        Rendered index.html template
    """
    return render_template('index.html')


# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle multiple file uploads from the form.
    Validates file types, saves them to the uploads folder,
    and extracts text using OCR from all files.
    Performs cross-paper analysis to detect repeated questions.
    Returns:
        Redirect to result page with aggregated analysis or error message
    """
    # Get list of uploaded files
    files = request.files.getlist('files')

    # Validate that files were uploaded
    if not files or len(files) == 0:
        flash('No files selected!', 'error')
        return redirect(url_for('index'))

    # Check if at least one file has a filename
    if all(f.filename == '' for f in files):
        flash('No files selected!', 'error')
        return redirect(url_for('index'))

    # Validate minimum 2 files requirement
    valid_files = [f for f in files if f.filename != '']
    if len(valid_files) < 2:
        flash(f'Please upload at least 2 question papers for analysis. You uploaded {len(valid_files)} file(s).', 'error')
        return redirect(url_for('index'))

    # Lists to store aggregated data
    all_questions = []
    all_tokens = []
    processed_files = []
    extraction_errors = []
    total_removed_lines = []  # Track removed instruction lines

    # Process each uploaded file
    for file in valid_files:
        # Check if file type is allowed
        if not allowed_file(file.filename):
            flash(f'Invalid file type for {file.filename}! Only PDF, JPG, JPEG, and PNG files are allowed.', 'error')
            continue

        try:
            # Secure the filename
            filename = secure_filename(file.filename)

            # Save file to uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract text from the file
            extracted_text = extract_text(filepath)

            # Apply NLP preprocessing for this file
            try:
                # Preprocess the extracted text
                cleaned_text, tokens = preprocess_text(extracted_text)

                # USE ADVANCED QUESTION EXTRACTOR (filters out instructions)
                extraction_result = extract_questions_advanced(extracted_text)
                questions = extraction_result['questions']
                removed_lines = extraction_result['removed_lines']

                # Track removed lines for debugging
                total_removed_lines.extend(removed_lines)

                # Aggregate data from this paper
                all_questions.extend(questions)
                all_tokens.extend(tokens)

                # Track successfully processed files with extraction stats
                processed_files.append({
                    'filename': filename,
                    'question_count': len(questions),
                    'token_count': len(tokens),
                    'removed_count': len(removed_lines)
                })

                print(f"✅ {filename}: {len(questions)} questions extracted, {len(removed_lines)} instruction lines removed")

            except Exception as nlp_error:
                print(f"NLP processing failed for {filename}: {nlp_error}")
                extraction_errors.append(f"{filename}: NLP processing failed")

        except Exception as e:
            print(f"Error processing {file.filename}: {str(e)}")
            extraction_errors.append(f"{file.filename}: {str(e)}")

    # Check if we have any successfully processed files
    if len(processed_files) == 0:
        flash('Failed to process any files. Please check file formats and try again.', 'error')
        return redirect(url_for('index'))

    # ═══════════════════════════════════════════════════════════════
    # NEW IMPROVED ANALYSIS PIPELINE
    # ═══════════════════════════════════════════════════════════════

    try:
        print("\n" + "=" * 60)
        print("🚀 STARTING IMPROVED ANALYSIS PIPELINE")
        print("=" * 60)

        total_papers = len(processed_files)

        # Step 1: Clean all questions (remove instruction noise)
        print("\n📋 Step 1: Cleaning extracted questions...")
        cleaned_questions = []
        for q in all_questions:
            cleaned = clean_question_text(q)
            if is_valid_question(cleaned):
                cleaned_questions.append(cleaned)

        print(f"   Original: {len(all_questions)} questions")
        print(f"   After cleaning: {len(cleaned_questions)} valid questions")

        # Step 2: Semantic similarity grouping (TF-IDF based)
        print("\n🔗 Step 2: Grouping similar questions...")
        question_groups = group_similar_questions(cleaned_questions, threshold=0.65)
        print(f"   Found {len(question_groups)} unique question groups")

        # Step 3: Find repeated questions
        print("\n🔄 Step 3: Identifying repeated questions...")
        repeated_questions = find_repeated_questions(cleaned_questions, min_occurrences=2, threshold=0.65)
        print(f"   Found {len(repeated_questions)} repeated questions")

        # Format repeated questions for display
        formatted_repeated = []
        for group in repeated_questions:
            level, label, color = classify_importance(group['count'], total_papers)
            formatted_repeated.append({
                'question': group['representative'],
                'frequency': group['count'],
                'variants': group['variants'][:3],
                'importance_level': level,
                'importance_label': label,
                'importance_color': color
            })

        # Step 4: Comprehensive topic analysis
        print("\n📊 Step 4: Analyzing topics...")
        topic_analysis = comprehensive_topic_analysis(cleaned_questions, total_papers)
        top_keywords = topic_analysis['top_keywords']

        # Step 5: Rank all questions by importance
        print("\n🏆 Step 5: Ranking questions by importance...")
        ranked_questions = rank_questions(question_groups, topic_analysis, total_papers)

        # Step 6: Generate Important Questions Report
        print("\n📝 Step 6: Generating important questions report...")
        important_report = get_important_questions_report(ranked_questions, top_n=20)

        # Step 7: Generate Practice Paper
        print("\n📄 Step 7: Generating practice paper...")
        practice_paper = generate_practice_paper(ranked_questions)

        # Legacy format for backwards compatibility with templates
        predicted_paper = {
            'section_a': practice_paper['section_a'],
            'section_b': practice_paper['section_b'],
            'section_c': practice_paper['section_c']
        }

        # Step 8: Generate PDFs
        print("\n📑 Step 8: Generating PDFs...")
        try:
            # Generate Practice Paper PDF
            pdf_path = create_pdf(predicted_paper)
            print(f"   ✅ Practice Paper PDF generated: {pdf_path}")

            # Generate Important Questions Report PDF
            report_pdf_path = create_important_questions_pdf(important_report)
            print(f"   ✅ Important Questions Report PDF generated: {report_pdf_path}")

            pdf_available = True
            report_pdf_available = True
        except Exception as pdf_error:
            print(f"   ⚠️ PDF generation failed: {pdf_error}")
            pdf_path = None
            report_pdf_path = None
            pdf_available = False
            report_pdf_available = False

        # Calculate statistics
        total_questions = len(all_questions)
        unique_questions = len(question_groups)
        total_tokens = len(all_tokens)
        files_processed = len(processed_files)

        # Format ranked questions for template (legacy format)
        formatted_ranked = [
            (q['question'], q['importance_score'], q['rank'])
            for q in ranked_questions
        ]

        print("\n" + "=" * 60)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"   Files processed: {files_processed}")
        print(f"   Total questions: {total_questions}")
        print(f"   Unique groups: {unique_questions}")
        print(f"   Repeated questions: {len(formatted_repeated)}")
        print("=" * 60)

        # Render result page with improved analysis
        return render_template('result.html',
                             files_processed=files_processed,
                             processed_files=processed_files,
                             total_questions=total_questions,
                             unique_questions=unique_questions,
                             repeated_questions=formatted_repeated,
                             total_tokens=total_tokens,
                             keywords=top_keywords,
                             ranked=formatted_ranked,
                             paper=predicted_paper,
                             practice_paper=practice_paper,
                             important_report=important_report,
                             topic_analysis=topic_analysis,
                             pdf_available=pdf_available,
                             report_pdf_available=report_pdf_available,
                             extraction_errors=extraction_errors)

    except Exception as e:
        flash(f'Analysis failed: {str(e)}', 'error')
        return redirect(url_for('index'))


# Route to download the generated PDF
@app.route('/download')
def download_pdf():
    """
    Send the generated PDF file to the user for download.
    Returns:
        PDF file download or error message if file doesn't exist
    """
    try:
        pdf_path = os.path.join('static', 'generated', 'predicted_paper.pdf')

        # Check if PDF exists
        if not os.path.exists(pdf_path):
            flash('PDF not found. Please generate a predicted paper first.', 'error')
            return redirect(url_for('index'))

        # Send file for download
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name='PrepVision_AI_Practice_Paper.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Error downloading PDF: {str(e)}', 'error')
        return redirect(url_for('index'))


# Route to download the Important Questions Report PDF
@app.route('/download-report')
def download_report_pdf():
    """
    Send the Important Questions Report PDF to the user for download.
    Returns:
        PDF file download or error message if file doesn't exist
    """
    try:
        pdf_path = os.path.join('static', 'generated', 'important_questions_report.pdf')

        # Check if PDF exists
        if not os.path.exists(pdf_path):
            flash('Important Questions Report PDF not found. Please analyze papers first.', 'error')
            return redirect(url_for('index'))

        # Send file for download
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name='PrepVision_AI_Important_Questions_Report.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Error downloading Report PDF: {str(e)}', 'error')
        return redirect(url_for('index'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

