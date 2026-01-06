import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def enhance_text_with_ai(text):
    if not text.strip():
        return ""

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        print("Warning: GOOGLE_API_KEY not found. Skipping AI enhancement.")
        return text

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        prompt = (
            "You will receive OCR-extracted text from a PDF. "
            "The text may contain OCR noise, broken line wraps, encoding artifacts, and page layout issues (e.g., multi-column text). "
            "First, detect the primary language of the document (e.g., Spanish, English, French, Portuguese, Italian, German). "
            "Use the detected language only to guide spelling, diacritics, and character normalization. "
            "Goal: produce a clean, readable version while preserving the original paragraph structure as closely as possible. "
            "Correct OCR transcription errors, including misspellings, broken words, and obvious character confusions "
            "(such as l/1, O/0, rn/m, etc.). "
            "Normalize encoding issues and diacritics according to the detected language. "
            "If accented characters or special letters are replaced by digits or symbols, correct them ONLY when unambiguous from context. "
            "Do not invent content. "
            "Remove repetitive headers, footers, page numbers, and running titles IF they are not part of the main body. "
            "Paragraphs and line breaks (critical): "
            "Preserve paragraph boundaries as in the original document. "
            "Use exactly one blank line between paragraphs. "
            "Do NOT merge distinct paragraphs. "
            "Return plain text only. "
            f"\n\n--- OCR TEXT ---\n{text}"
        )

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=2048,
                temperature=0.2
            )
        )

        if response and response.candidates:
            return response.candidates[0].content.parts[0].text

    except Exception as e:
        print(f"Error during AI text enhancement: {e}")
        return text

    return text
