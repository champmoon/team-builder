from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin

from .exercises_types import ExercisesTypes


class Exercises(Base, UUIDAsIDMixin):
    __tablename__ = "exercises"

    workout_pool_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="workouts_pool.id",
            ondelete="CASCADE",
        )
    )
    type_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="exercises_types.id",
            ondelete="CASCADE",
        )
    )
    reps: Mapped[int | None]
    sets: Mapped[int | None]
    rest: Mapped[float | None]
    time: Mapped[int | None]
    order: Mapped[int]

    type: Mapped[ExercisesTypes] = relationship(
        lazy="immediate",
        viewonly=True,
    )
