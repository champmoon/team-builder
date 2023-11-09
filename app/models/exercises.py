from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class Exercises(Base, UUIDAsIDMixin):
    __tablename__ = "exercises"

    workout_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="workouts.id",
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
    rest: Mapped[int | None]
    time: Mapped[int | None]
    order: Mapped[int]
