from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class Workouts(Base, UUIDAsIDMixin):
    __tablename__ = "workouts"

    name: Mapped[str]
    estimated_time: Mapped[float]
    date: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
