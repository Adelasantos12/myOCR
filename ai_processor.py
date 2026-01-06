import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def enhance_text_with_ai(text):
    """
    Enhances the given text by correcting transcription errors, removing headers/footers,
    and improving overall formatting for better readability.

    If the GOOGLE_API_KEY is not set, it returns the original text.
    """
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
    "Do NOT mention the detected language in the output. "

    "Goal: produce a clean, readable version while preserving the original paragraph structure as closely as possible. "

    "Correct OCR transcription errors, including misspellings, broken words, and obvious character confusions "
    "(such as l/1, O/0, rn/m, etc.). "

    "Normalize encoding issues and diacritics according to the detected language. "
    "If accented characters or special letters are replaced by digits or symbols, correct them ONLY when unambiguous from context. "
    "Do not invent content. "

    "Remove repetitive headers, footers, page numbers, and running titles IF they are not part of the main body. "

    "Layout robustness (multi-column, footnotes, tables): "
    "If the text appears to come from two or more columns, reconstruct the most plausible reading order by grouping lines that belong together "
    "based on semantic continuity, punctuation, and consistent topic flow. "
    "Avoid merging lines from different columns or unrelated segments. "
    "If a sequence seems interleaved (e.g., alternating unrelated lines), prefer keeping them as separate paragraphs rather than forcing a merge. "
    "If footnotes/endnotes are present (often marked by numbers, symbols, or short lines), keep them attached to the nearest relevant paragraph "
    "only if the association is clear; otherwise move them to the end under a 'Notes' section without changing their text. "
    "If tabular content is detected (rows/columns separated by spacing), preserve it in a simple, readable plain-text form, keeping rows on separate lines. "

    "Paragraphs and line breaks (critical): "
    "Preserve paragraph boundaries as in the original document. "
    "Use exactly one blank line between paragraphs. "
    "Do NOT merge distinct paragraphs. "

    "Fix line breaks carefully: "
    "If a line break is caused only by visual line wrapping within the same paragraph, merge it by replacing the newline with a single space. "
    "Do NOT merge if doing so would join unrelated fragments (a common symptom of multi-column OCR). "
    "Preserve real paragraph breaks, usually indicated by a blank line or strong structural cues (heading, numbering reset, topic shift). "

    "Preserve headings, lists, bullet points, and numbering on separate lines. "

    "Handle hyphenation correctly: "
    "If a word is split across lines due to wrapping (e.g., 'inter-\\nnational'), merge it into one word. "
    "If the hyphen is semantically meaningful (e.g., 'COVID-19'), preserve it. "

    "Output rules: "
    "Return plain text only. "
    "Use exactly one blank line between paragraphs. "
    "Do not add explanations, comments, labels, or markdown. "
    "Do not surround the output with quotes. "

    f"\n\n--- OCR TEXT ---\n{text}"
)

        response = model.generate_content(prompt,
                                          generation_config=genai.types.GenerationConfig(
                                              candidate_count=1,
                                              max_output_tokens=2048,
                                              temperature=0.2))

        if response and response.candidates:
            return response.candidates[0].content.parts[0].text

    except Exception as e:
        print(f"Error during AI text enhancement: {e}")
        # Fallback to original text in case of an API error
        return text

    # Fallback if the response is empty or malformed
    return text
