# Import necessary libraries
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import pdfplumber

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
    Handle file upload from the form.
    Validates file type, saves it to the uploads folder,
    and extracts text using OCR.
    Returns:
        Redirect to result page with extracted text or error message
    """
    # Check if file is present in request
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    # Check if user selected a file
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('index'))

    # Check if file type is allowed
    if file and allowed_file(file.filename):
        # Secure the filename to prevent malicious file names
        filename = secure_filename(file.filename)

        # Save file to uploads folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Extract text from the uploaded file
            extracted_text = extract_text(filepath)

            # Render result page with extracted text
            return render_template('result.html',
                                   filename=filename,
                                   extracted_text=extracted_text)

        except Exception as e:
            # Handle OCR errors
            flash(f'File uploaded but text extraction failed: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type! Only PDF, JPG, JPEG, and PNG files are allowed.', 'error')
        return redirect(url_for('index'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

