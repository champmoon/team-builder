from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class StressQuestionnaires(Base, UUIDAsIDMixin):
    __tablename__ = "stress_questionnaires"

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
    rating: Mapped[int]
    text: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class HealthQuestionnaires(Base, UUIDAsIDMixin):
    __tablename__ = "health_questionnaires"

    sportsman_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="sportsmans.id",
            ondelete="CASCADE",
        )
    )
    rating: Mapped[int]
    text: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
