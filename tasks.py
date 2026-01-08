import os
import shutil
import tempfile
from layout_extractor import convert_pdf_to_images, analyze_layout_and_ocr
from docx_builder import build_docx_from_structure

def process_pdf_layout_aware(filepath: str, original_filename: str):
    """
    Processes a PDF file using a layout-aware pipeline to generate a
    structured DOCX file.
    """
    temp_dir = tempfile.mkdtemp()

    try:
        print(f"Starting layout-aware processing for {original_filename}")

        # 1. Convert PDF to images
        image_paths = convert_pdf_to_images(filepath, temp_dir)

        if not image_paths:
            raise Exception("PDF to image conversion failed to produce any images.")

        # 2. Analyze layout and perform OCR on images
        structured_document = analyze_layout_and_ocr(image_paths)

        if not structured_document or not any(page.get('blocks') for page in structured_document):
            raise Exception("Layout analysis failed to extract any document structure with blocks.")

        # 3. Build the DOCX from the structured data
        base_filename = os.path.splitext(original_filename)[0]
        docx_filename = f"{base_filename}_structured.docx"
        docx_output_path = os.path.join('results', docx_filename)

        build_docx_from_structure(structured_document, docx_output_path)

        txt_output_path = None

        return {
            'status': 'SUCCESS',
            'message': 'Successfully processed the document with layout analysis.',
            'txt_path': txt_output_path,
            'docx_path': docx_output_path,
            'text': ""
        }

    except Exception as e:
        print(f"An error occurred during layout-aware processing: {e}")
        return {
            'status': 'ERROR',
            'message': str(e),
            'txt_path': None,
            'docx_path': None
        }
    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")

process_pdf = process_pdf_layout_aware
