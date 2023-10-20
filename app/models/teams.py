from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin

from .sportsmans import Sportsmans


class Teams(Base, UUIDAsIDMixin):
    __tablename__ = "teams"

    trainer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="trainers.id",
            ondelete="CASCADE",
        )
    )
    sportsmans: Mapped[list[Sportsmans]] = relationship(
        lazy="immediate",
        viewonly=True,
    )
