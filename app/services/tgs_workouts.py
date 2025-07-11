from typing import Sequence
from uuid import UUID

from app import schemas
from app.models import TGSWorkouts
from app.repositories import TGSWorkoutsRepository


class TGSWorkoutsService:
    def __init__(self, repository: TGSWorkoutsRepository) -> None:
        self.repository = repository

    async def get_by_workout_id(self, workout_id: UUID) -> TGSWorkouts | None:
        return await self.repository.get_by_workout_id(workout_id=workout_id)

    async def get_by_all_sportsman_id(
        self, sportsman_id: UUID
    ) -> Sequence[TGSWorkouts]:
        return await self.repository.get_all_by_sportsman_id(sportsman_id=sportsman_id)

    async def get_all_by_team_id(self, team_id: UUID) -> Sequence[TGSWorkouts]:
        return await self.repository.get_all_by_team_id(team_id=team_id)

    async def get_all_by_group_id(self, group_id: UUID) -> Sequence[TGSWorkouts]:
        return await self.repository.get_all_by_group_id(group_id=group_id)

    async def create(self, schema_in: schemas.CreateTGSWorkoutIn) -> TGSWorkouts:
        return await self.repository.create(schema_in=schema_in)

    async def delete(self, id: UUID) -> TGSWorkouts:
        return await self.repository.delete(id=id)

    async def get_future_group_workouts_ids(self, group_id: UUID) -> Sequence[UUID]:
        return await self.repository.get_future_group_workouts_ids(group_id=group_id)

    async def get_future_team_workouts_ids(self, team_id: UUID) -> Sequence[UUID]:
        return await self.repository.get_future_team_workouts_ids(team_id=team_id)

    async def merge(
        self,
        local_sportsman_id: UUID,
        true_sportsman_id: UUID,
    ) -> None:
        return await self.repository.merge(
            local_sportsman_id=local_sportsman_id,
            true_sportsman_id=true_sportsman_id,
        )
