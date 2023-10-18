from sqlalchemy.orm import Mapped

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class Admins(Base, UUIDAsIDMixin):
    __tablename__ = "admins"

    email: Mapped[str]
    hashed_password: Mapped[str]
