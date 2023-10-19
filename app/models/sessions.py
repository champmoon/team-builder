from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.consts import UsersTypes
from app.db.base_class import Base
from app.db.mixins import UUIDAsIDMixin


class Sessions(Base, UUIDAsIDMixin):
    __tablename__ = "sessions"

    user_id: Mapped[UUID]
    refresh_token: Mapped[UUID]
    user_type: Mapped[UsersTypes]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
