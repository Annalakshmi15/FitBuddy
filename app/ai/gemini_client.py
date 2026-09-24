from google import genai

from app.config import settings


def get_gemini_client() -> genai.Client:
    """
    Create and return a Gemini API client.

    The API key is loaded from the .env file through application settings.
    """

    if not settings.GEMINI_API_KEY.strip():
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(
        api_key=settings.GEMINI_API_KEY.strip()
    )