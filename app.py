# Import necessary libraries
from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import pdfplumber

# Import NLP preprocessing functions
from modules.preprocessing import preprocess_text, extract_questions, analyze_topics

# Import question paper generator
from modules.generator import generate_predicted_paper

# Import PDF generator
from modules.pdf_generator import create_pdf

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
        flash(f'Please upload at least 2 question papers. You uploaded {len(valid_files)} file(s).', 'error')
        return redirect(url_for('index'))

    # Lists to store aggregated data
    all_questions = []
    all_tokens = []
    processed_files = []
    extraction_errors = []

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

                # Extract questions from this paper
                questions = extract_questions(extracted_text)

                # Aggregate data from this paper
                all_questions.extend(questions)
                all_tokens.extend(tokens)

                # Track successfully processed files
                processed_files.append({
                    'filename': filename,
                    'question_count': len(questions),
                    'token_count': len(tokens)
                })

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

    # Perform cross-paper analysis
    try:
        from collections import Counter

        # Detect repeated questions using fuzzy matching on cleaned questions
        # Normalize questions for comparison (lowercase, strip whitespace)
        normalized_questions = {}
        for q in all_questions:
            # Create normalized version for comparison
            normalized = ' '.join(q.lower().split())
            if normalized not in normalized_questions:
                normalized_questions[normalized] = {
                    'original': q,
                    'count': 0
                }
            normalized_questions[normalized]['count'] += 1

        # Find repeated questions (appearing in multiple papers)
        repeated_questions = [
            {
                'question': data['original'],
                'frequency': data['count']
            }
            for norm_q, data in normalized_questions.items()
            if data['count'] > 1
        ]

        # Sort by frequency (most repeated first)
        repeated_questions.sort(key=lambda x: x['frequency'], reverse=True)

        # Analyze topics across all papers
        topic_analysis = analyze_topics(all_tokens, all_questions)
        top_keywords = topic_analysis['top_keywords']
        ranked_questions = topic_analysis['ranked_questions']

        # Generate predicted question paper from ranked questions
        predicted_paper = generate_predicted_paper(ranked_questions, top_keywords)

        # Generate PDF version of the predicted paper
        try:
            pdf_path = create_pdf(predicted_paper)
            print(f"✅ PDF generated successfully: {pdf_path}")
            pdf_available = True
        except Exception as pdf_error:
            print(f"⚠️ PDF generation failed: {pdf_error}")
            pdf_path = None
            pdf_available = False

        # Calculate statistics
        total_questions = len(all_questions)
        unique_questions = len(normalized_questions)
        total_tokens = len(all_tokens)
        files_processed = len(processed_files)

        # Render result page with cross-paper analysis and predicted paper
        return render_template('result.html',
                             files_processed=files_processed,
                             processed_files=processed_files,
                             total_questions=total_questions,
                             unique_questions=unique_questions,
                             repeated_questions=repeated_questions,
                             total_tokens=total_tokens,
                             keywords=top_keywords,
                             ranked=ranked_questions,
                             paper=predicted_paper,
                             pdf_available=pdf_available,
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
            download_name='PrepVision_AI_Predicted_Paper.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Error downloading PDF: {str(e)}', 'error')
        return redirect(url_for('index'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

