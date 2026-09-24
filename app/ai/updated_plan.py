from app.ai.gemini_client import get_gemini_client
from app.config import settings
from app.schemas import UserInput, WorkoutPlan


SAFETY_INSTRUCTION = """
You are FitBuddy, a general wellness and fitness planning assistant.

Safety rules:
- Provide general fitness and wellness information only.
- Do not diagnose medical conditions.
- Do not prescribe medical treatment.
- Do not recommend starvation or extreme dieting.
- Do not recommend dangerous exercises.
- Do not provide calorie restriction targets.
- Do not recommend supplements.
- Do not make unrealistic transformation promises.
- Respect the user's feedback while keeping the revised plan safe.
"""


def generate_updated_plan(
    user: UserInput,
    original_plan: WorkoutPlan,
    feedback: str,
) -> WorkoutPlan:
    """
    Generate an updated workout plan based on the user's feedback.
    """

    client = get_gemini_client()

    original_plan_json = original_plan.model_dump_json(
        indent=2
    )

    prompt = f"""
{SAFETY_INSTRUCTION}

Create a revised 7-day workout plan.

User information:
Name: {user.name}
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Intensity: {user.intensity}
Preferences: {user.preferences or "None"}

Original workout plan:
{original_plan_json}

User feedback:
{feedback}

Instructions:
1. Understand the user's feedback.
2. Modify the original plan accordingly.
3. Keep exactly 7 days.
4. Keep the plan suitable for the selected intensity.
5. Keep exercise instructions simple.
6. Preserve useful parts of the original plan when possible.
7. Do not provide calorie restriction targets.
8. Do not recommend supplements.
9. Do not provide medical diagnosis or treatment.
10. Return ONLY the structured JSON output.

Required JSON structure:
- title
- overview
- days

Each day:
- day
- focus
- exercises

Each exercise:
- name
- duration
- instructions
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
            "Gemini returned an empty updated workout plan."
        )

    return WorkoutPlan.model_validate_json(response.text)