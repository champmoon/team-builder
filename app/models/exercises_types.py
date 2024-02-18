from sqlalchemy.orm import Mapped

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class ExercisesTypes(Base, UUIDAsIDMixin):
    __tablename__ = "exercises_types"

    type: Mapped[int]
