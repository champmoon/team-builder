import asyncio
import logging

from app import schemas
from app.conf.settings import settings
from app.db.session import DB
from app.models import Admins
from app.repositories import AdminsRepository
from app.services.admins import AdminsService

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def first_admin() -> None:
    admin_service = AdminsService(
        repository=AdminsRepository(
            model=Admins,
            session_factory=DB().session,
        )
    )
    admin_out = await admin_service.get_by_email(settings.FIRST_ADMIN_EMAIL)

    if not admin_out:
        new_admin_out = await admin_service.create(
            schemas.CreateAdminIn(
                email=settings.FIRST_ADMIN_EMAIL,
                password=settings.FIRST_ADMIN_PASSWORD,
            )
        )
        logger.info(f"First admin created with email - {new_admin_out.email}")


if __name__ == "__main__":
    asyncio.run(first_admin())
