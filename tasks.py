import os
import traceback
from layout_extractor import extractor
from docx_builder import builder

def process_pdf(filepath, original_filename):
    """
    Processes a PDF file, extracts text using docTR OCR, and saves it to a text file and a Word document.
    """
    print(f"Starting OCR processing for {filepath}")

    os.makedirs('results', exist_ok=True)

    try:
        base_filename = os.path.splitext(original_filename)[0]
        output_txt_path = os.path.join('results', f"{base_filename}.txt")
        output_docx_path = os.path.join('results', f"{base_filename}.docx")

        # 1. Extract layout and text using docTR
        # Note: extractor.process_pdf uses docTR which handles PDF to image internally
        result = extractor.process_pdf(filepath)
        full_text = extractor.get_full_text(result)
        structured_data = extractor.to_structured_data(result)

        if not full_text.strip():
            print("Warning: Extracted text is empty.")
            return {
                'status': 'ERROR',
                'message': 'OCR processing resulted in empty text. The document might not contain any machine-readable text.'
            }

        # 2. Save text file
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        # 3. Build DOCX using the structured data
        builder.build_docx(structured_data, output_docx_path)

        print(f"Finished processing for {filepath}")
        return {
            'status': 'SUCCESS',
            'txt_path': output_txt_path,
            'docx_path': output_docx_path,
            'text': full_text
        }
    except Exception as e:
        print(f"An error occurred during process_pdf: {e}")
        traceback.print_exc()
        return {'status': 'ERROR', 'message': str(e)}
