from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin

from .sportsmans import Sportsmans


class Groups(Base, UUIDAsIDMixin):
    __tablename__ = "groups"

    trainer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="trainers.id",
            ondelete="CASCADE",
        )
    )
    name: Mapped[str]
    sportsmans: Mapped[list[Sportsmans]] = relationship(
        secondary="sportsmans_groups",
        lazy="immediate",
        viewonly=True,
    )
