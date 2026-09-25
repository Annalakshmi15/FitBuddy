import json

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.ai.gemini_flash_generator import generate_nutrition_recovery_tip
from app.ai.gemini_generator import generate_workout_plan
from app.ai.updated_plan import generate_updated_plan
from app.database import FitnessUser, get_db
from app.schemas import FeedbackRequest, UserInput, WorkoutPlan


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


def render_error(
    request: Request,
    message: str,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": message,
        },
        status_code=400,
    )


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None,
        },
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse,
)
async def generate_workout(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    preferences: str = Form(""),
    db: Session = Depends(get_db),
):
    """
    Receive user data, validate it, generate the workout plan,
    generate the nutrition/recovery tip, save everything to SQLite,
    and display result.html.
    """

    try:
        user_input = UserInput(
            name=name.strip(),
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            preferences=preferences.strip(),
        )
    except Exception as exc:
        return render_error(
            request,
            f"Please check your input: {exc}",
        )

    try:
        workout_plan = generate_workout_plan(
            user_input
        )

        nutrition_tip = generate_nutrition_recovery_tip(
            user_input
        )

        db_user = FitnessUser(
            name=user_input.name,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
            preferences=user_input.preferences,
            original_plan=workout_plan.model_dump_json(),
            updated_plan="",
            nutrition_tip=nutrition_tip,
            feedback="",
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": db_user,
                "plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "updated": False,
                "error": None,
            },
        )

    except Exception as exc:
        db.rollback()

        return render_error(
            request,
            f"Unable to generate the plan. {exc}",
        )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse,
)
async def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Receive feedback, retrieve the original plan,
    generate an updated plan, save it, and display it.
    """

    try:
        feedback_data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback.strip(),
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": None,
                "plan": None,
                "nutrition_tip": "",
                "updated": False,
                "error": f"Invalid feedback: {exc}",
            },
            status_code=400,
        )

    db_user = db.get(
        FitnessUser,
        feedback_data.user_id,
    )

    if db_user is None:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": None,
                "plan": None,
                "nutrition_tip": "",
                "updated": False,
                "error": "User record was not found.",
            },
            status_code=404,
        )

    try:
        original_plan = WorkoutPlan.model_validate(
            json.loads(db_user.original_plan)
        )

        user_input = UserInput(
            name=db_user.name,
            age=db_user.age,
            weight=db_user.weight,
            goal=db_user.goal,
            intensity=db_user.intensity,
            preferences=db_user.preferences,
        )

        updated_plan = generate_updated_plan(
            user=user_input,
            original_plan=original_plan,
            feedback=feedback_data.feedback,
        )

        db_user.updated_plan = (
            updated_plan.model_dump_json()
        )

        db_user.feedback = feedback_data.feedback

        db.commit()
        db.refresh(db_user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": db_user,
                "plan": updated_plan,
                "nutrition_tip": db_user.nutrition_tip,
                "updated": True,
                "error": None,
            },
        )

    except Exception as exc:
        db.rollback()

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": db_user,
                "plan": None,
                "nutrition_tip": db_user.nutrition_tip,
                "updated": False,
                "error": f"Unable to update the plan. {exc}",
            },
            status_code=500,
        )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse,
)
async def view_all_users(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Display all saved users and their plans.
    """

    result = db.execute(
        select(FitnessUser).order_by(
            FitnessUser.created_at.desc()
        )
    )

    users = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
        },
    )