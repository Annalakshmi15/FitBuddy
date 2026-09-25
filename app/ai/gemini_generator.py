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
    If Gemini is temporarily unavailable, use a local demo plan.
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

    # Local demo fallback used when Gemini is temporarily unavailable.
    return WorkoutPlan(
        title="7-Day General Wellness Plan",
        overview="A simple beginner-friendly home wellness plan with movement, recovery, and rest.",
        days=[
            {
                "day": "Day 1",
                "focus": "Full Body Movement",
                "exercises": [
                    {
                        "name": "Warm-up",
                        "duration": "5 minutes",
                        "instructions": "Gentle walking and easy mobility movements.",
                    },
                    {
                        "name": "Bodyweight Squats",
                        "duration": "10 minutes",
                        "instructions": "Perform comfortable controlled squats with good posture.",
                    },
                ],
            },
            {
                "day": "Day 2",
                "focus": "Upper Body and Mobility",
                "exercises": [
                    {
                        "name": "Arm Circles",
                        "duration": "5 minutes",
                        "instructions": "Move the arms gently in controlled circles.",
                    },
                    {
                        "name": "Wall Push-ups",
                        "duration": "10 minutes",
                        "instructions": "Use a wall for support and perform comfortable repetitions.",
                    },
                ],
            },
            {
                "day": "Day 3",
                "focus": "Light Cardio",
                "exercises": [
                    {
                        "name": "Easy Walking",
                        "duration": "15 minutes",
                        "instructions": "Walk at a comfortable pace.",
                    },
                ],
            },
            {
                "day": "Day 4",
                "focus": "Recovery and Stretching",
                "exercises": [
                    {
                        "name": "Gentle Stretching",
                        "duration": "10 minutes",
                        "instructions": "Perform comfortable stretches without forcing the movement.",
                    },
                ],
            },
            {
                "day": "Day 5",
                "focus": "Lower Body Movement",
                "exercises": [
                    {
                        "name": "Chair Squats",
                        "duration": "10 minutes",
                        "instructions": "Use a chair for support and perform controlled movements.",
                    },
                ],
            },
            {
                "day": "Day 6",
                "focus": "Light Mobility",
                "exercises": [
                    {
                        "name": "Gentle Mobility",
                        "duration": "10 minutes",
                        "instructions": "Move the shoulders, hips, and ankles gently.",
                    },
                    {
                        "name": "Easy Walking",
                        "duration": "10 minutes",
                        "instructions": "Walk comfortably and focus on relaxed movement.",
                    },
                ],
            },
            {
                "day": "Day 7",
                "focus": "Rest and Recovery",
                "exercises": [
                    {
                        "name": "Relaxed Stretching",
                        "duration": "5 minutes",
                        "instructions": "Perform gentle stretching and allow the body to recover.",
                    },
                ],
            },
        ],
    )