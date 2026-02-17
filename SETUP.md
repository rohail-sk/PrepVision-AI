# PrepVision AI - Setup Guide

## 🚀 Quick Setup Instructions

### Step 1: Install Python Dependencies

```bash
cd "C:\Users\Rohail\Desktop\3rd year project\PrepVision AI"
pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR (Required for Image OCR)

**For Windows:**

1. **Download Tesseract OCR:**
   - Visit: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.3.3.exe`)

2. **Install Tesseract:**
   - Run the installer
   - **Important**: Note the installation path (default: `C:\Program Files\Tesseract-OCR`)
   - Make sure to check "Add to PATH" during installation

3. **Configure Tesseract Path in app.py:**
   - Open `app.py`
   - Find line 9 (after imports)
   - Uncomment and update the path if Tesseract is not in PATH:
   
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Step 3: Verify Installation

```bash
# Test if Tesseract is accessible
tesseract --version
```

If you see the version number, Tesseract is correctly installed!

### Step 4: Run the Application

```bash
python app.py
```

### Step 5: Access the Application

Open your browser and go to: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
PrepVision AI/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── OCR_FEATURES.md            # Features documentation
├── SETUP.md                   # This file
│
├── templates/
│   ├── index.html             # Upload page
│   └── result.html            # Text extraction result page
│
├── static/                    # Static files (CSS, JS, images)
│
└── uploads/                   # Uploaded files storage
```

---

## 🧪 Testing the Application

### Test with Image Files:
1. Upload a JPG/PNG image with text
2. Wait for OCR processing
3. View extracted text on result page

### Test with PDF Files:
1. Upload a PDF document
2. Wait for text extraction
3. View extracted text (page by page) on result page

---

## ⚠️ Troubleshooting

### Error: "TesseractNotFoundError"
**Solution:**
- Tesseract is not installed or not in PATH
- Install Tesseract from the link above
- Configure the path in `app.py` line 9

### Error: "No module named 'pytesseract'"
**Solution:**
```bash
pip install pytesseract==0.3.10
```

### Error: "No module named 'PIL'"
**Solution:**
```bash
pip install Pillow==10.0.0
```

### Error: "No module named 'pdfplumber'"
**Solution:**
```bash
pip install pdfplumber==0.10.3
```

### Poor OCR Quality
**Solutions:**
- Use high-resolution images
- Ensure good contrast and clear text
- Use images with minimal background noise
- Consider image preprocessing (future enhancement)

---

## 🎯 Features

✅ Upload PDF, JPG, JPEG, PNG files  
✅ Automatic OCR text extraction  
✅ Page-by-page PDF text extraction  
✅ Image text extraction using Tesseract  
✅ Beautiful UI with flash messages  
✅ Error handling and validation  
✅ Scrollable text display  
✅ Secure file handling  

---

## 🔧 Configuration Options

### Maximum File Size
Edit in `app.py` line 20:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Allowed File Types
Edit in `app.py` line 16:
```python
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
```

### Upload Folder
Edit in `app.py` line 15:
```python
UPLOAD_FOLDER = 'uploads'
```

---

## 📝 Next Steps (Optional Enhancements)

- [ ] Add image preprocessing for better OCR
- [ ] Support for more file formats (DOCX, TXT)
- [ ] Download extracted text as TXT file
- [ ] Multiple file upload support
- [ ] OCR language selection
- [ ] Text analysis and keyword extraction
- [ ] Question paper pattern analysis

---

## 📞 Support

If you encounter any issues, check:
1. All dependencies are installed (`pip list`)
2. Tesseract OCR is installed and accessible
3. Virtual environment is activated (if using)
4. Python version is 3.7 or higher

---

**Happy Coding! 🎉**

