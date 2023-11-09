from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class TrainersWorkouts(Base, UUIDAsIDMixin):
    __tablename__ = "trainers_workouts"

    trainer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="trainers.id",
            ondelete="CASCADE",
        )
    )
    workout_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="workouts.id",
            ondelete="CASCADE",
        )
    )
    status_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="workouts_statuses.id",
            ondelete="CASCADE",
        )
    )
