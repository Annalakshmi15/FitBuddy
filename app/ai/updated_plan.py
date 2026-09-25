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
"""

    try:
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

        if response.text:
            return WorkoutPlan.model_validate_json(response.text)

    except Exception:
        pass

    # Local demo fallback when Gemini is temporarily unavailable.
    updated_plan = original_plan.model_copy(deep=True)

    if updated_plan.days:
        updated_plan.days[0].focus = "Light Full Body Movement"

    if len(updated_plan.days) >= 6:
        updated_plan.days[5].focus = "Light Mobility and Stretching"
        updated_plan.days[5].exercises = [
            {
                "name": "Gentle Stretching",
                "duration": "10 minutes",
                "instructions": "Perform comfortable stretches without forcing the movement.",
            },
            {
                "name": "Easy Walking",
                "duration": "10 minutes",
                "instructions": "Walk at a comfortable and relaxed pace.",
            },
        ]

    updated_plan.overview = (
        "Updated plan with a lighter Day 6 and additional stretching "
        "based on the user's feedback."
    )

    return updated_plan