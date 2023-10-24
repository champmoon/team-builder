from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class SportsmansTrainigs(Base, UUIDAsIDMixin):
    __tablename__ = "sportsmans_trainigs"

    sportsman_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="sportsmans.id",
            ondelete="CASCADE",
        )
    )
    trainig_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="trainigs.id",
            ondelete="CASCADE",
        )
    )
    status_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="trainigs_statuses.id",
            ondelete="CASCADE",
        )
    )
    execution_time: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
