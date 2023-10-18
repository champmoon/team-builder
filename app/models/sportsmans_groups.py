from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class SportsmansGroups(Base, UUIDAsIDMixin):
    __tablename__ = "sportsmans_groups"

    sportsman_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="sportsmans.id",
            ondelete="CASCADE",
        )
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="groups.id",
            ondelete="CASCADE",
        )
    )
