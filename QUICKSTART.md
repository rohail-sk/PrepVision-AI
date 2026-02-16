# Quick Start Guide for PrepVision AI

## Running the Application

### Option 1: Using Command Prompt
1. Open Command Prompt
2. Navigate to the project folder:
   ```
   cd "C:\Users\Rohail\Desktop\3rd year project\PrepVision AI"
   ```
3. Run the app:
   ```
   python app.py
   ```
4. Open browser and visit: http://127.0.0.1:5000/

### Option 2: Using PowerShell
1. Open PowerShell
2. Navigate to the project folder:
   ```
   cd "C:\Users\Rohail\Desktop\3rd year project\PrepVision AI"
   ```
3. Run the app:
   ```
   python app.py
   ```
4. Open browser and visit: http://127.0.0.1:5000/

## What You Should See

When you run `python app.py`, you should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

## Testing the Application

1. The homepage will display "PrepVision AI - Question Paper Predictor"
2. Click the upload area to select a file
3. Choose a PDF or image file (supported: PDF, JPG, JPEG, PNG)
4. Click "Upload & Predict"
5. You should see a green success message: "File uploaded successfully!"
6. The file will be saved in the `uploads/` folder

## Important Notes

- The server runs on **port 5000** by default
- The application is in **debug mode** (auto-reloads on code changes)
- Maximum file size is **16MB**
- Only **PDF, JPG, JPEG, PNG** files are accepted
- Files are automatically renamed securely to prevent security issues

## Stopping the Server

Press `Ctrl + C` in the terminal/command prompt where the server is running.

## Common Issues

**Issue**: "Address already in use"
**Fix**: Another program is using port 5000. Either:
- Stop that program, or
- Change the port in app.py: `app.run(debug=True, port=5001)`

**Issue**: "No module named 'flask'"
**Fix**: Install Flask: `pip install flask`

**Issue**: Files are not uploading
**Fix**: 
- Check that `uploads/` folder exists
- Check file permissions
- Try a smaller file (under 16MB)
- Ensure file type is PDF, JPG, JPEG, or PNG

