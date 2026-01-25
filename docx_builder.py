from docx import Document
from docx.shared import Pt

class DocxBuilder:
    def __init__(self):
        pass

    def build_docx(self, structured_pages, output_path):
        """
        Builds a DOCX file from structured page data.
        structured_pages is a list of pages, where each page is a list of blocks,
        and each block is a list of lines (strings).
        """
        print(f"Building DOCX at {output_path}...")
        doc = Document()

        # Set default style
        style = doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)

        for i, page in enumerate(structured_pages):
            for block in page:
                # We could potentially use block coordinates to try and maintain layout
                # but for now, we'll just group lines into paragraphs.
                # A block in docTR is usually a paragraph or a coherent text region.

                # Join lines in a block with spaces to form a paragraph
                paragraph_text = " ".join(block)
                if paragraph_text.strip():
                    doc.add_paragraph(paragraph_text)

            if i < len(structured_pages) - 1:
                doc.add_page_break()

        doc.save(output_path)
        return output_path

# Global instance for reuse
builder = DocxBuilder()
