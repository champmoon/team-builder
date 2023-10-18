from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class Sportsmans(Base, UUIDAsIDMixin):
    __tablename__ = "sportsmans"

    team_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="teams.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        default=None,
    )
    email: Mapped[str]
    hashed_password: Mapped[str]

    name: Mapped[str]
