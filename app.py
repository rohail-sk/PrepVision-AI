# Import necessary libraries
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

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
    Validates file type and saves it to the uploads folder.
    Returns:
        Redirect to homepage with success or error message
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

        flash(f'File "{filename}" uploaded successfully!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type! Only PDF, JPG, JPEG, and PNG files are allowed.', 'error')
        return redirect(url_for('index'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

