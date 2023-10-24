from sqlalchemy.orm import Mapped

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class WorkoutsStatuses(Base, UUIDAsIDMixin):
    __tablename__ = "workouts_statuses"

    status: Mapped[int]
