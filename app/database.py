from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

from app.config import settings


# SQLite needs this option when used with FastAPI.
connect_args = {}

if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


class FitnessUser(Base):
    __tablename__ = "fitness_users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    goal: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    intensity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    preferences: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    original_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    updated_plan: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    feedback: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


def create_tables() -> None:
    """
    Create all database tables if they do not already exist.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Provide a database session to FastAPI routes.
    """
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()