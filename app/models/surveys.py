from sqlalchemy.orm import Mapped, mapped_column, Mapper
from sqlalchemy import ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Connection
from uuid import UUID

from app.db.mixins import UUIDAsIDMixin

from sqlalchemy import event, insert
from .teams import Teams


class TeamSurveys(Base, UUIDAsIDMixin):
    __tablename__ = "team_surveys"

    team_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="teams.id",
            ondelete="CASCADE",
        )
    )
    main_fields: Mapped[dict | list[dict]] = mapped_column(JSONB, server_default="[]")
    add_fields: Mapped[dict | list[dict]] = mapped_column(JSONB, server_default="[]")


class SportsmanSurveys(Base, UUIDAsIDMixin):
    __tablename__ = "sportsman_surveys"

    sportsman_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="sportsmans.id",
            ondelete="CASCADE",
        )
    )
    update_it: Mapped[bool] = mapped_column(default=True)
    answers: Mapped[list[dict]] = mapped_column(JSONB)
