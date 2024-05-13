from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class ExercisesTypes(Base, UUIDAsIDMixin):
    __tablename__ = "exercises_types"

    type: Mapped[int]
    description: Mapped[str]
    is_basic: Mapped[bool]

    trainer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="trainers.id",
            ondelete="CASCADE",
        )
    )
