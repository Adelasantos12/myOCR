import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the generative AI model with the API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please create a .env file and add it.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def enhance_text_with_ai(text):
    """
    Enhances the given text by correcting transcription errors, removing headers/footers,
    and improving overall formatting for better readability.
    """
    if not text.strip():
        return ""

    prompt = (
        "Please process the following OCR-extracted text from a scanned document. "
        "Your task is to correct any transcription errors, remove any headers, footers, "
        "or page numbers, and format the text to be clean and readable while preserving "
        "the original's paragraph structure and justification. "
        "Ensure the output is a single, continuous block of text, ready for a DOCX file."
        f"\n\n--- OCR Text ---\n{text}"
    )

    try:
        response = model.generate_content(prompt,
                                          generation_config=genai.types.GenerationConfig(
                                              candidate_count=1,
                                              stop_sequences=['\n\n\n'],
                                              max_output_tokens=2048,
                                              temperature=0.2))  # Lower temperature for more deterministic output

        # Check if the response has the expected structure
        if response and response.candidates:
            # Prioritize the text from the first candidate
            return response.candidates[0].content.parts[0].text.strip()

    except Exception as e:
        print(f"Error during AI text enhancement: {e}")
        # Fallback to original text in case of an API error
        return text

    # Fallback if the response is empty or malformed
    return text
