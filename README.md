# PDF OCR Web Application

This is a simple web application that allows you to upload a scanned PDF, performs Optical Character Recognition (OCR) on it, and returns the extracted text as both a `.txt` and a `.docx` file.

## How to Run the Application

This is a Python project built with the Flask framework. You will need Python and `pip` installed.

### 1. Install System Dependencies

This application uses the Tesseract OCR engine. You must install it on your system.

On Debian/Ubuntu-based systems, you can install it with:
```bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr
```

### 2. Install Python Dependencies

All the required Python libraries are listed in the `requirements.txt` file. Install them using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Run the Web Server

Once the dependencies are installed, you can start the Flask web server with the following command:
```bash
python app.py
```

You should see output indicating that the server is running, similar to this:
```
 * Running on http://127.0.0.1:5000
```

### 4. Access the Application

Open your web browser and navigate to the URL shown in the terminal (usually `http://127.0.0.1:5000`) to use the application.
