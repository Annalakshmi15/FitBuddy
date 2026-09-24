from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserInput(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    age: int = Field(
        ge=13,
        le=100,
    )

    weight: float = Field(
        gt=0,
        le=500,
    )

    goal: Literal[
        "Weight Loss",
        "Muscle Gain",
        "General Wellness",
    ]

    intensity: Literal[
        "Beginner",
        "Moderate",
        "Advanced",
    ]

    preferences: str = Field(
        default="",
        max_length=1000,
    )


class FeedbackRequest(BaseModel):
    user_id: int = Field(
        gt=0,
    )

    feedback: str = Field(
        min_length=3,
        max_length=2000,
    )


class Exercise(BaseModel):
    name: str
    duration: str
    instructions: str


class WorkoutDay(BaseModel):
    day: str
    focus: str
    exercises: list[Exercise]


class WorkoutPlan(BaseModel):
    title: str
    overview: str
    days: list[WorkoutDay]


class UserRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    weight: float
    goal: str
    intensity: str
    preferences: str
    original_plan: str
    updated_plan: str
    nutrition_tip: str
    feedback: str
    created_at: str