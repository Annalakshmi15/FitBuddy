from app.ai.gemini_client import get_gemini_client
from app.config import settings
from app.schemas import UserInput


def generate_nutrition_recovery_tip(user: UserInput) -> str:
    """
    Generate a short general nutrition/recovery tip using Gemini Flash.
    """

    client = get_gemini_client()

    prompt = f"""
You are the nutrition and recovery assistant for FitBuddy.

Provide one concise, practical wellness tip for this user.

User:
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Intensity: {user.intensity}
Preferences: {user.preferences or "None"}

Safety requirements:
- Give general wellness information only.
- Do not diagnose medical conditions.
- Do not prescribe treatment.
- Do not give calorie restriction targets.
- Do not recommend starvation or extreme dieting.
- Do not recommend supplements.
- Do not make unrealistic body transformation claims.
- Focus on ordinary balanced food habits, hydration, sleep,
  rest, and recovery.
- Keep the response short and beginner-friendly.

Return only the tip as plain text.
"""

    response = client.models.generate_content(
        model=settings.GEMINI_FLASH_MODEL,
        contents=prompt,
        config={}
    )

    tip = (response.text or "").strip()

    if not tip:
        raise RuntimeError(
            "Gemini Flash returned an empty nutrition/recovery tip."
        )

    return tip