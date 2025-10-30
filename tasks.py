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

    os.makedirs('results', exist_ok=True)

    try:
        base_filename = os.path.splitext(original_filename)[0]
        output_txt_path = os.path.join('results', f"{base_filename}.txt")
        output_docx_path = os.path.join('results', f"{base_filename}.docx")

        full_text = ""
        doc = fitz.open(filepath)
        document = docx.Document()

        print(f"PDF has {len(doc)} pages.")

        for page_num in range(len(doc)):
            print(f"Processing page {page_num + 1}...")
            page = doc.load_page(page_num)

            pix = page.get_pixmap(dpi=600)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.convert('L')
            img = img.point(lambda x: 0 if x < 180 else 255, '1')

            # Use Tesseract to extract text, specifying Spanish and English languages
            try:
                text = pytesseract.image_to_string(img, lang='spa+eng')
                print(f"  > Extracted text (page {page_num + 1}, length {len(text)}): '{text[:100].strip()}...'")
                full_text += text + "\n\n"

                for paragraph in text.split('\n'):
                    document.add_paragraph(paragraph)
                document.add_page_break()
            except pytesseract.TesseractNotFoundError:
                print("  > TESSERACT NOT FOUND. Make sure it's installed and in your PATH.")
                raise
            except Exception as e:
                print(f"  > Error during OCR on page {page_num + 1}: {e}")
                continue

        print(f"Total extracted text length: {len(full_text)}")

        if not full_text.strip():
            print("Warning: Extracted text is empty. The PDF might be image-only without readable text.")
            return {
                'status': 'ERROR',
                'message': 'OCR processing resulted in empty text. The document might not contain any machine-readable text.'
            }

        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        document.save(output_docx_path)

        print(f"Finished processing for {filepath}")
        return {
            'status': 'SUCCESS',
            'txt_path': output_txt_path,
            'docx_path': output_docx_path,
            'text': full_text
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'status': 'ERROR', 'message': str(e)}
