# from uuid import UUID

# from app.consts import WorkoutsStatusesEnum

# from .health_questionnaires import create_health_questionnaire
# from .workout_status import skip_workout_sportsman, skip_workout_trainer,
# start_workout


# async def dispath_tasks(key: str) -> None:
#     match key.split("_"):
#         case "pre", "health", "questionnaire", sportsman_id:
#             await create_health_questionnaire(sportsman_id=UUID(sportsman_id))

#         case WorkoutsStatusesEnum.PLANNED.name, _, workout_id:
#             await start_workout(workout_id=UUID(workout_id))

#         case (
#             WorkoutsStatusesEnum.SKIPPED.name,
#             _,
#             workout_id,
#             "sportsman",
#             sportsman_id,
#         ):
#             await skip_workout_sportsman(
#                 workout_id=UUID(workout_id), sportsman_id=UUID(sportsman_id)
#             )

#         case (
#             WorkoutsStatusesEnum.SKIPPED.name,
#             _,
#             workout_id,
#             "trainer",
#             trainer_id,
#         ):
#             await skip_workout_trainer(
#                 workout_id=UUID(workout_id), trainer_id=UUID(trainer_id)
#             )
