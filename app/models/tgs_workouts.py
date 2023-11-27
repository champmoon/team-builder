from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class TGSWorkouts(Base, UUIDAsIDMixin):
    __tablename__ = "tgs_workouts"

    team_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            column="teams.id",
            ondelete="CASCADE",
        )
    )
    group_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            column="groups.id",
            ondelete="CASCADE",
        )
    )
    sportsman_id: Mapped[UUID | None] = mapped_column(
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
