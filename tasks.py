import time
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from ai_processor import enhance_text_with_ai

def process_pdf(filepath, original_filename):
    """
    Processes a PDF file, extracts text using OCR, enhances it with AI,
    and saves it to a text file and a formatted Word document.
    """
    print(f"Starting OCR processing for {filepath}")

    os.makedirs('results', exist_ok=True)

    try:
        base_filename = os.path.splitext(original_filename)[0]
        output_txt_path = os.path.join('results', f"{base_filename}.txt")
        output_docx_path = os.path.join('results', f"{base_filename}.docx")

        full_text = ""
        doc = fitz.open(filepath)

        print(f"PDF has {len(doc)} pages.")

        for page_num in range(len(doc)):
            print(f"Processing page {page_num + 1}...")
            page = doc.load_page(page_num)

            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Use Tesseract to extract text
            try:
                text = pytesseract.image_to_string(img, lang='eng+spa')
                print(f"  > Extracted text (page {page_num + 1}, length {len(text)}): '{text[:100].strip()}...'")
                full_text += text + "\n"
            except pytesseract.TesseractNotFoundError:
                print("  > TESSERACT NOT FOUND. Make sure it's installed and in your PATH.")
                raise
            except Exception as e:
                print(f"  > Error during OCR on page {page_num + 1}: {e}")
                continue

        print(f"Total extracted text length: {len(full_text)}")

        if not full_text.strip():
            print("Warning: Extracted text is empty.")
            return {
                'status': 'ERROR',
                'message': 'OCR processing resulted in empty text. The document might not contain readable text.'
            }

        # Enhance the extracted text with AI
        print("Enhancing text with AI...")
        enhanced_text = enhance_text_with_ai(full_text)
        print(f"Enhanced text length: {len(enhanced_text)}")

        # Save the raw and enhanced text to a .txt file
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write("--- Original OCR Text ---\n")
            f.write(full_text)
            f.write("\n\n--- Enhanced Text ---\n")
            f.write(enhanced_text)

        # Create and save the formatted .docx file
        document = docx.Document()
        for paragraph_text in enhanced_text.split('\n'):
            if paragraph_text.strip():
                p = document.add_paragraph(paragraph_text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        document.save(output_docx_path)

        print(f"Finished processing for {filepath}")
        return {
            'status': 'SUCCESS',
            'txt_path': output_txt_path,
            'docx_path': output_docx_path,
            'text': enhanced_text
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'status': 'ERROR', 'message': str(e)}
