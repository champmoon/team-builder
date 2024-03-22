from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin

from .workouts_statuses import WorkoutsStatuses


class SportsmansWorkouts(Base, UUIDAsIDMixin):
    __tablename__ = "sportsmans_workouts"

    sportsman_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="sportsmans.id",
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
    execution_time: Mapped[float | None] = mapped_column(default=None)

    status: Mapped[WorkoutsStatuses] = relationship(
        lazy="immediate",
        viewonly=True,
    )
