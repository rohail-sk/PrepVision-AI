# PrepVision AI - Question Paper Predictor

A Flask-based web application for AI-powered question paper prediction.

## Features

✅ Upload PDF or image files (JPG, JPEG, PNG)
✅ File type validation
✅ Secure filename handling
✅ Beautiful, responsive UI
✅ Flash messages for user feedback
✅ Maximum file size: 16MB

## Project Structure

```
PrepVision AI/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── uploads/              # Uploaded files storage
├── templates/            # HTML templates
│   └── index.html       # Homepage template
└── static/              # Static files (CSS, JS, images)
```

## Installation

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Install Flask**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install Flask
   ```

## How to Run

1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```bash
   cd "C:\Users\Rohail\Desktop\3rd year project\PrepVision AI"
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

5. To stop the server, press `Ctrl + C` in the terminal

## Usage

1. Click on the upload area to select a file
2. Choose a PDF or image file (PDF, JPG, JPEG, or PNG)
3. Click "Upload & Predict" button
4. You'll see a success message if the file was uploaded successfully

## File Upload Details

- **Allowed file types:** PDF, JPG, JPEG, PNG
- **Maximum file size:** 16MB
- **Storage location:** `uploads/` folder
- **Filename security:** Automatically secured using `secure_filename()`

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Template Engine:** Jinja2
- **File Handling:** Werkzeug

## Future Enhancements

- [ ] AI/ML integration for question paper analysis
- [ ] Preview uploaded files
- [ ] Delete uploaded files
- [ ] Export predictions to PDF
- [ ] User authentication
- [ ] Database integration

## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'flask'`
**Solution:** Run `pip install Flask`

**Problem:** Port 5000 is already in use
**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

**Problem:** Files not uploading
**Solution:** Check that the `uploads/` folder exists and has write permissions

## License

This project is created for educational purposes.

## Author

Created for 3rd Year Project - 2026

