from uuid import UUID as _py_uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as _psql_uuid
from sqlalchemy.orm import Mapped, mapped_column


class UUIDAsIDMixin:
    id: Mapped[_py_uuid] = mapped_column(
        _psql_uuid(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
