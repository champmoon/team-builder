from sqlalchemy.orm import Mapped

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class Trainers(Base, UUIDAsIDMixin):
    __tablename__ = "trainers"

    email: Mapped[str]
    hashed_password: Mapped[str]

    first_name: Mapped[str | None]
    middle_name: Mapped[str | None]
    last_name: Mapped[str | None]
