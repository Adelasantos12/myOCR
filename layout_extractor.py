import fitz  # PyMuPDF
import os
from typing import List, Dict, Any
import numpy as np
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# --- Part 1: PDF to Image Conversion ---

def convert_pdf_to_images(pdf_path: str, output_folder: str) -> List[str]:
    """Converts each page of a PDF file into a high-resolution PNG image."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_paths = []
    try:
        doc = fitz.open(pdf_path)
        zoom_matrix = fitz.Matrix(3.0, 3.0)  # ~216 DPI

        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=zoom_matrix)
            image_path = os.path.join(output_folder, f"page_{i+1}.png")
            pix.save(image_path)
            image_paths.append(image_path)

        print(f"Successfully converted {len(doc)} pages to images.")

    except Exception as e:
        print(f"An error occurred during PDF to image conversion: {e}")
        raise
    finally:
        if 'doc' in locals() and doc:
            doc.close()

    return image_paths

# --- Part 2: Layout Analysis and OCR ---

def analyze_layout_and_ocr(image_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Analyzes images to detect layout, extract text blocks, and perform OCR.
    """
    structured_document = []
    model = ocr_predictor(pretrained=True)

    for page_num, img_path in enumerate(image_paths):
        img = DocumentFile.from_images(img_path)[0]
        result = model([img])

        page_blocks = []
        page_height, page_width = img.shape[:2]

        # Heuristic to find average block height for title detection
        block_heights = [
            (block.geometry[1][1] - block.geometry[0][1]) * page_height
            for block in result.pages[0].blocks
        ]
        avg_block_height = np.mean(block_heights) if block_heights else 30

        # 1. Extract and initially classify blocks
        for block in result.pages[0].blocks:
            (x0, y0), (x1, y1) = block.geometry
            text = " ".join([line.render() for line in block.lines])
            confidence = np.mean([word.confidence for line in block.lines for word in line.words]) if block.lines else 0.0
            abs_bbox = [x0 * page_width, y0 * page_height, x1 * page_width, y1 * page_height]

            # Header/Footer suppression is disabled for now
            # if abs_bbox[1] < header_margin or abs_bbox[3] > footer_margin:
            #     continue

            # 3. Simple block type classification heuristic
            block_type = "paragraph"
            block_height = abs_bbox[3] - abs_bbox[1]
            if block_height > avg_block_height * 1.8 and page_num == 0:
                block_type = "title"
            elif block_height > avg_block_height * 1.5:
                block_type = "heading"

            page_blocks.append({
                "type": block_type,
                "bbox": [round(c, 2) for c in abs_bbox],
                "text": text,
                "confidence": round(confidence, 4)
            })

        # 4. Deterministic sorting
        page_blocks.sort(key=lambda b: (round(b['bbox'][1] / 20), b['bbox'][0]))

        structured_document.append({
            "page": page_num + 1,
            "blocks": page_blocks
        })

    return structured_document
