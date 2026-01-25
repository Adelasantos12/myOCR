import os
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

class LayoutExtractor:
    def __init__(self):
        print("Initializing docTR predictor...")
        # docTR will use PyTorch backend as installed
        self.predictor = ocr_predictor(pretrained=True)

    def process_pdf(self, pdf_path):
        """
        Processes a PDF and returns the docTR result.
        """
        print(f"Extracting layout from {pdf_path}...")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Load the PDF
        doc = DocumentFile.from_pdf(pdf_path)

        # Perform OCR
        result = self.predictor(doc)
        return result

    def to_structured_data(self, result):
        """
        Converts docTR result to a simplified structured format.
        """
        structured_pages = []
        for page in result.pages:
            blocks = []
            for block in page.blocks:
                lines = []
                for line in block.lines:
                    words = [word.value for word in line.words]
                    lines.append(" ".join(words))
                blocks.append(lines)
            structured_pages.append(blocks)
        return structured_pages

    def get_full_text(self, result):
        """
        Returns the full text from the result.
        """
        full_text = ""
        for page in result.pages:
            for block in page.blocks:
                for line in block.lines:
                    line_text = " ".join([word.value for word in line.words])
                    full_text += line_text + "\n"
                full_text += "\n"
            full_text += "\n--- Page Break ---\n\n"
        return full_text

# Global instance for reuse
extractor = LayoutExtractor()
