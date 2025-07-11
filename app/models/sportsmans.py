from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class Sportsmans(Base, UUIDAsIDMixin):
    __tablename__ = "sportsmans"

    team_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            column="teams.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        default=None,
    )
    email: Mapped[str | None]
    hashed_password: Mapped[str | None]

    first_name: Mapped[str | None]
    middle_name: Mapped[str | None]
    last_name: Mapped[str | None]

    avatar_uri: Mapped[str | None]

    groups: Mapped[list["Groups"]] = relationship(  # type: ignore  # noqa
        secondary="sportsmans_groups",
        lazy="immediate",
        viewonly=True,
    )
