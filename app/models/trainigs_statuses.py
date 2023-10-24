from sqlalchemy.orm import Mapped

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class TrainigsStatuses(Base, UUIDAsIDMixin):
    __tablename__ = "trainigs_statuses"

    status: Mapped[int]
