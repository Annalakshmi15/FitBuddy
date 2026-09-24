from app.ai.gemini_client import get_gemini_client
from app.config import settings
from app.schemas import UserInput, WorkoutPlan


SAFETY_INSTRUCTION = """
You are FitBuddy, a general wellness and fitness planning assistant.

Important safety rules:
- Give general wellness and fitness education only.
- Do not diagnose medical conditions.
- Do not prescribe medical treatment.
- Do not recommend starvation, fasting for weight loss, extreme dieting,
  dangerous exercise, or unrealistic body transformation.
- Do not provide calorie restriction targets.
- Do not recommend supplements.
- Do not make promises about exact weight loss or body transformation.
- Keep exercise suggestions appropriate for the user's selected intensity.
- Include simple warm-up, exercise, and recovery guidance.
- If the user's preferences suggest a potentially unsafe activity,
  replace it with a safer general alternative.
- Keep the plan practical and understandable.
"""


def generate_workout_plan(user: UserInput) -> WorkoutPlan:
    """
    Generate a structured 7-day fitness plan using Gemini.
    """

    client = get_gemini_client()

    prompt = f"""
Create a safe, practical 7-day general wellness fitness plan.

User:
Name: {user.name}
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Intensity: {user.intensity}
Preferences: {user.preferences or "None"}

Requirements:
- Exactly 7 days.
- Each day needs a focus and exercises.
- Each exercise needs a name, duration, and short instructions.
- Include rest/recovery where appropriate.
- No calorie targets.
- No supplements.
- No medical diagnosis or treatment.
- Keep the plan appropriate for the selected intensity.
- Return only the structured JSON output.
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": WorkoutPlan,
        },
    )

    if getattr(response, "parsed", None) is not None:
        parsed = response.parsed

        if isinstance(parsed, WorkoutPlan):
            return parsed

        return WorkoutPlan.model_validate(parsed)

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty workout plan."
        )

    return WorkoutPlan.model_validate_json(response.text)