import time
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
import docx

def process_pdf(filepath, original_filename):
    """
    Processes a PDF file, extracts text using OCR, and saves it to a text file and a Word document.
    """
    print(f"Starting OCR processing for {filepath}")

    # Ensure the results directory exists
    os.makedirs('results', exist_ok=True)

    try:
        # Generate a unique name for the output file
        base_filename = os.path.splitext(original_filename)[0]
        output_txt_path = os.path.join('results', f"{base_filename}.txt")
        output_docx_path = os.path.join('results', f"{base_filename}.docx")

        full_text = ""

        # Open the PDF file
        doc = fitz.open(filepath)

        # Create a new Word document
        document = docx.Document()

        # Iterate through each page of the PDF
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Render the page as a high-resolution image (300 DPI is good for OCR)
            pix = page.get_pixmap(dpi=300)

            # Convert the pixmap to a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Use Tesseract to extract text from the image
            text = pytesseract.image_to_string(img)
            full_text += text + "\n\n"  # Add page breaks

            # Add the text to the Word document, preserving paragraphs
            for paragraph in text.split('\n'):
                document.add_paragraph(paragraph)
            document.add_page_break()

        # Save the extracted text to a .txt file
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        # Save the Word document
        document.save(output_docx_path)

        print(f"Finished processing for {filepath}")
        return {
            'status': 'SUCCESS',
            'txt_path': output_txt_path,
            'docx_path': output_docx_path
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'status': 'ERROR', 'message': str(e)}
