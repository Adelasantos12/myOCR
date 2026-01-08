from docx import Document
from docx.shared import Inches
from typing import List, Dict, Any

def build_docx_from_structure(structured_data: List[Dict[str, Any]], output_path: str):
    """
    Builds a DOCX document from a structured representation of a document.

    Args:
        structured_data: A list of page dictionaries, each containing a list of
                         text blocks with type, text, and other metadata.
        output_path: The file path where the generated DOCX will be saved.
    """
    document = Document()

    # Basic style configuration (can be expanded)
    try:
        title_style = document.styles['Title']
        heading_style = document.styles['Heading 1']
    except KeyError:
        # Fallback if styles are not in the default template
        title_style = document.styles['Normal']
        heading_style = document.styles['Normal']

    total_pages = len(structured_data)
    for i, page in enumerate(structured_data):
        print(f"Building page {page.get('page', 'N/A')}...")
        for block in page.get('blocks', []):
            block_type = block.get("type", "paragraph")
            text = block.get("text", "")

            if not text.strip():
                continue

            # Map block type to a document element and style
            if block_type == "title":
                p = document.add_paragraph(text, style=title_style)
            elif block_type == "heading":
                p = document.add_paragraph(text, style=heading_style)
            else: # Default to paragraph
                p = document.add_paragraph(text)

        # Add a page break after each page's content, except for the last one
        if (i + 1) < total_pages:
            document.add_page_break()

    try:
        document.save(output_path)
        print(f"DOCX file successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving DOCX file: {e}")
        raise
