from app.utils.router import EndPointRouter, url

from . import docs, endpoints

trainer_urls_router = EndPointRouter()
sportsman_urls_router = EndPointRouter()


url.POST("    /auth/login                           ", endpoint=endpoints.general.auth.login, docs=docs.general.login)
url.POST("    /auth/logout                          ", endpoint=endpoints.general.auth.logout, docs=docs.general.logout)
url.POST("    /auth/refresh                         ", endpoint=endpoints.general.auth.refresh, docs=docs.general.refresh)
url.POST("    /auth/verify                          ", endpoint=endpoints.general.auth.verify, docs=docs.general.verify)

url.POST("    /trainer/register                     ", endpoint=endpoints.trainers.auth.register_trainer, docs=docs.trainers.register_trainer)
url.POST("    /trainer/email                        ", endpoint=endpoints.trainers.auth.send_confirm_trainer_email, docs=docs.trainers.send_confirm_trainer_email)
url.POST("    /trainer/email/confirm                ", endpoint=endpoints.trainers.auth.confirm_trainer_email, docs=docs.trainers.confirm_trainer_email)

url.POST("    /sportsman/register                   ", endpoint=endpoints.sportsmans.auth.register_sportsman, docs=docs.sportsmans.register_sportsman)
url.POST("    /sportsman/email                      ", endpoint=endpoints.sportsmans.auth.send_confirm_sportsman_email, docs=docs.sportsmans.send_confirm_sportsman_email)
url.POST("    /sportsman/email/confirm              ", endpoint=endpoints.sportsmans.auth.confirm_sportsman_email, docs=docs.sportsmans.confirm_sportsman_email)

url.GET("     /trainer/profile                      ", endpoint=endpoints.trainers.profile.get_profile, docs=docs.trainers.get_profile)
url.PATCH("   /trainer/profile                      ", endpoint=endpoints.trainers.profile.update_profile, docs=docs.trainers.update_profile)
url.POST("    /trainer/profile/avatar               ", endpoint=endpoints.trainers.profile.upload_avatar, docs=docs.trainers.upload_avatar)

url.GET("     /sportsman/profile                    ", endpoint=endpoints.sportsmans.profile.get_profile, docs=docs.sportsmans.get_profile)
url.PATCH("   /sportsman/profile                    ", endpoint=endpoints.sportsmans.profile.update_profile, docs=docs.sportsmans.update_profile)
url.POST("    /sportsman/profile/avatar             ", endpoint=endpoints.sportsmans.profile.upload_avatar, docs=docs.trainers.upload_avatar)

url.GET("     /trainer/team                         ", endpoint=endpoints.trainers.teams.get_self_team, docs=docs.trainers.get_self_team)
url.POST("    /trainer/team/add                     ", endpoint=endpoints.trainers.teams.add_sportsman_to_team, docs=docs.trainers.add_sportsman_to_team)
url.POST("    /trainer/team/adds                    ", endpoint=endpoints.trainers.teams.adds_sportsmans_to_team, docs=docs.trainers.adds_sportsmans_to_team,)
url.POST("    /trainer/team/kick                    ", endpoint=endpoints.trainers.teams.kick_sportsman_off_team, docs=docs.trainers.kick_sportsman_off_team)
url.POST("    /trainer/team/kicks                   ", endpoint=endpoints.trainers.teams.kicks_sportsmans_off_team, docs=docs.trainers.kicks_sportsmans_off_team)

url.GET("     /sportsman/team                       ", endpoint=endpoints.sportsmans.teams.get_self_team, docs=docs.sportsmans.teams.get_self_team)
url.POST("    /sportsman/team/out                   ", endpoint=endpoints.sportsmans.teams.out_off_team, docs=docs.sportsmans.teams.out_off_team)

url.GET("     /trainer/groups                       ", endpoint=endpoints.trainers.groups.get_self_groups, docs=docs.trainers.get_self_groups)
url.GET("     /trainer/groups/{id}                  ", endpoint=endpoints.trainers.groups.get_self_group, docs=docs.trainers.get_self_group)
url.PATCH("   /trainer/groups/{id}                  ", endpoint=endpoints.trainers.groups.update_group, docs=docs.trainers.update_group)
url.DELETE("  /trainer/groups/{id}                  ", endpoint=endpoints.trainers.groups.delete_group, docs=docs.trainers.delete_group)
url.POST("    /trainer/groups                       ", endpoint=endpoints.trainers.groups.create_group, docs=docs.trainers.create_group)
url.POST("    /trainer/groups/add                   ", endpoint=endpoints.trainers.groups.add_sportsman_to_group, docs=docs.trainers.add_sportsman_to_group)
url.POST("    /trainer/groups/adds                  ", endpoint=endpoints.trainers.groups.adds_sportsmans_to_group, docs=docs.trainers.adds_sportsmans_to_group)
url.POST("    /trainer/groups/kick                  ", endpoint=endpoints.trainers.groups.kick_sportsman_off_group, docs=docs.trainers.kick_sportsman_off_group)
url.POST("    /trainer/groups/kicks                 ", endpoint=endpoints.trainers.groups.kicks_sportsmans_off_group, docs=docs.trainers.kicks_sportsmans_off_group)

url.GET("     /sportsman/groups                     ", endpoint=endpoints.sportsmans.groups.get_self_groups, docs=docs.sportsmans.get_self_groups)
url.GET("     /sportsman/groups/{id}                ", endpoint=endpoints.sportsmans.groups.get_self_group, docs=docs.sportsmans.get_self_group)
url.POST("    /sportsman/groups/outs                ", endpoint=endpoints.sportsmans.groups.outs_off_groups, docs=docs.sportsmans.outs_off_groups)
url.POST("    /sportsman/groups/out/{id}            ", endpoint=endpoints.sportsmans.groups.out_off_group, docs=docs.sportsmans.out_off_group)

url.GET("     /exercises/types                      ", endpoint=endpoints.general.exercises_types.get_exercises_types, docs=docs.general.get_exercises_types)

url.POST("    /trainer/workout/sportsman            ", endpoint=endpoints.trainers.workouts.create_workout_for_sportsman, docs=docs.trainers.create_workout_for_sportsman)
url.GET("     /trainer/workout/sportsman/{email}    ", endpoint=endpoints.trainers.workouts.get_workouts_for_sportsman, docs=docs.trainers.get_workouts_for_sportsman)
url.POST("    /trainer/workout/group                ", endpoint=endpoints.trainers.workouts.create_workout_for_group, docs=docs.trainers.create_workout_for_group)
url.GET("     /trainer/workout/group/{id}           ", endpoint=endpoints.trainers.workouts.get_workouts_for_group, docs=docs.trainers.get_workouts_for_group)
url.POST("    /trainer/workout/team                 ", endpoint=endpoints.trainers.workouts.create_workout_for_team, docs=docs.trainers.create_workout_for_team)
url.GET("     /trainer/workout/team                 ", endpoint=endpoints.trainers.workouts.get_workouts_for_team, docs=docs.trainers.get_workouts_for_team)
url.GET("     /trainer/workouts                     ", endpoint=endpoints.trainers.workouts.get_workouts, docs=docs.trainers.get_workouts)
url.GET("     /trainer/workouts/{id}                ", endpoint=endpoints.trainers.workouts.get_workout, docs=docs.trainers.get_workout)
url.DELETE("  /trainer/workouts/{id}                ", endpoint=endpoints.trainers.workouts.delete_workout, docs=docs.trainers.delete_workout)


trainer_urls_router.include_router(endpoints.trainers.auth.router, tags=[docs.tags_mapper["auth"]])
trainer_urls_router.include_router(endpoints.general.auth.router, tags=[docs.tags_mapper["auth"]])
trainer_urls_router.include_router(endpoints.general.exercises_types.router, tags=[docs.tags_mapper["exercises"]])
trainer_urls_router.include_router(endpoints.trainers.profile.router, tags=[docs.tags_mapper["trainers_profile"]])
trainer_urls_router.include_router(endpoints.trainers.teams.router, tags=[docs.tags_mapper["trainers_teams"]])
trainer_urls_router.include_router(endpoints.trainers.groups.router, tags=[docs.tags_mapper["trainers_groups"]])
trainer_urls_router.include_router(endpoints.trainers.workouts.router, tags=[docs.tags_mapper["trainers_workouts"]])


sportsman_urls_router.include_router(endpoints.sportsmans.auth.router, tags=[docs.tags_mapper["auth"]])
sportsman_urls_router.include_router(endpoints.general.auth.router, tags=[docs.tags_mapper["auth"]])
sportsman_urls_router.include_router(endpoints.general.exercises_types.router, tags=[docs.tags_mapper["exercises"]])
sportsman_urls_router.include_router(endpoints.sportsmans.profile.router, tags=[docs.tags_mapper["sportsmans_profile"]])
sportsman_urls_router.include_router(endpoints.sportsmans.teams.router, tags=[docs.tags_mapper["sportsmans_teams"]])
sportsman_urls_router.include_router(endpoints.sportsmans.groups.router, tags=[docs.tags_mapper["sportsmans_groups"]])
