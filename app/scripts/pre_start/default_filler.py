import asyncio
import logging

from app import schemas
from app.conf.settings import settings
from app.consts.sports_types import SportsTypes
from app.db.session import DB
from app.models import Trainers, Teams, ExercisesTypes, Sportsmans
from app.repositories import (
    TrainersRepository,
    TeamsRepository,
    ExercisesTypesRepository,
    SportsmansRepository,
)
from app.services.trainers import TrainersService
from app.services.teams import TeamsService
from app.services.exercises_types import ExercisesTypesService
from app.services.sportsmans import SportsmansService

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

FIRST_TRAINER_EMAIL = "trainer@trainer.com"
FIRST_TRAINER_PASSWORD = "trainer"

FIRST_TEAM_NAME = "team"
FIRST_TEAM_SPORT_TYPE = SportsTypes.BASKETBALL

FIRST_SPORTSMAN_EMAIL = "sportsman@sportsman.com"
FIRST_SPORTSMAN_PASSWORD = "sportsman"


async def first_trainer() -> Trainers:
    trainer_service = TrainersService(
        repository=TrainersRepository(
            model=Trainers,
            session_factory=DB().session,
        )
    )

    trainer_out = await trainer_service.get_by_email(FIRST_TRAINER_EMAIL)

    if not trainer_out:
        trainer_out = await trainer_service.create(
            schemas.CreateTrainerIn(
                email=FIRST_TRAINER_EMAIL,
                password=FIRST_TRAINER_PASSWORD,
            )
        )
        logger.info(f"First trainer created with email - {trainer_out.email}")

    ex_types_service = ExercisesTypesService(
        repository=ExercisesTypesRepository(
            model=ExercisesTypes,
            session_factory=DB().session,
        )
    )

    await ex_types_service.initialize_defaults(trainer_id=trainer_out.id)

    return trainer_out


async def first_team(trainer: Trainers) -> Teams:
    team_service = TeamsService(
        repository=TeamsRepository(
            model=Teams,
            session_factory=DB().session,
        )
    )

    team_out = await team_service.get_by_trainer_id(trainer.id)
    if not team_out:
        team_out = await team_service.create(
            schemas.CreateTeamIn(
                trainer_id=trainer.id,
                name=FIRST_TEAM_NAME,
                sport_type=FIRST_TEAM_SPORT_TYPE,
            )
        )
        logger.info(f"First team created with name - {team_out.name}")

    return team_out


async def first_sportsman(team: Teams) -> Sportsmans:
    sportsman_service = SportsmansService(
        repository=SportsmansRepository(
            model=Sportsmans,
            session_factory=DB().session,
        )
    )

    sportsman_out = await sportsman_service.get_by_email(FIRST_SPORTSMAN_EMAIL)
    if not sportsman_out:
        sportsman_out = await sportsman_service.create(
            schemas.CreateSportsmanIn(
                team_id=team.id,
                email=FIRST_SPORTSMAN_EMAIL,
                password=FIRST_SPORTSMAN_PASSWORD,
            )
        )
        logger.info(f"First sportsman created with email - {sportsman_out.email}")

    return sportsman_out


async def default_filler() -> None:
    trainer_out = await first_trainer()
    team_out = await first_team(trainer_out)
    await first_sportsman(team_out)


if __name__ == "__main__":
    asyncio.run(default_filler())
