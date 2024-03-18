from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin
from sqlalchemy import ForeignKey

from .exercises import Exercises


class WorkoutsPool(Base, UUIDAsIDMixin):
    __tablename__ = "workouts_pool"

    name: Mapped[str]
    estimated_time: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_visible: Mapped[bool] = mapped_column(default=True)

    trainer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="trainers.id",
            ondelete="CASCADE",
        )
    )
    exercises: Mapped[list[Exercises]] = relationship(lazy="immediate", viewonly=True)


class Workouts(Base, UUIDAsIDMixin):
    __tablename__ = "workouts"

    date: Mapped[datetime]
    workout_pool_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="workouts_pool.id",
            ondelete="CASCADE",
        )
    )
    workout_pool: Mapped[WorkoutsPool] = relationship(lazy="immediate", viewonly=True)
