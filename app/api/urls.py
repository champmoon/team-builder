from app.utils.router import EndPointRouter, url

from . import docs, endpoints

urls_router = EndPointRouter()

# General Auth
url.POST("    /auth/login                           ", endpoint=endpoints.general.auth.login, docs=docs.general.login)
url.POST("    /auth/logout                          ", endpoint=endpoints.general.auth.logout, docs=docs.general.logout)
url.POST("    /auth/refresh                         ", endpoint=endpoints.general.auth.refresh, docs=docs.general.refresh)
url.POST("    /auth/verify                          ", endpoint=endpoints.general.auth.verify, docs=docs.general.verify)

# General Exercises Types
url.GET("     /exercises/types                      ", endpoint=endpoints.general.exercises_types.get_exercises_types, docs=docs.general.get_exercises_types)

# Trainer Register
url.POST("    /trainer/register                     ", endpoint=endpoints.trainers.auth.register_trainer, docs=docs.trainers.register_trainer)
url.POST("    /trainer/email                        ", endpoint=endpoints.trainers.auth.send_confirm_trainer_email, docs=docs.trainers.send_confirm_trainer_email)
url.POST("    /trainer/email/confirm                ", endpoint=endpoints.trainers.auth.confirm_trainer_email, docs=docs.trainers.confirm_trainer_email)

# Sportsman Register
url.POST("    /sportsman/register                   ", endpoint=endpoints.sportsmans.auth.register_sportsman, docs=docs.sportsmans.register_sportsman)
url.POST("    /sportsman/email                      ", endpoint=endpoints.sportsmans.auth.send_confirm_sportsman_email, docs=docs.sportsmans.send_confirm_sportsman_email)
url.POST("    /sportsman/email/confirm              ", endpoint=endpoints.sportsmans.auth.confirm_sportsman_email, docs=docs.sportsmans.confirm_sportsman_email)

# Trainer Profile
url.GET("     /trainer/profile                      ", endpoint=endpoints.trainers.profile.get_profile, docs=docs.trainers.get_profile)
url.PATCH("   /trainer/profile                      ", endpoint=endpoints.trainers.profile.update_profile, docs=docs.trainers.update_profile)
url.POST("    /trainer/profile/avatar               ", endpoint=endpoints.trainers.profile.upload_avatar, docs=docs.trainers.upload_avatar)

# Sportsman Profile
url.GET("     /sportsman/profile                    ", endpoint=endpoints.sportsmans.profile.get_profile, docs=docs.sportsmans.get_profile)
url.PATCH("   /sportsman/profile                    ", endpoint=endpoints.sportsmans.profile.update_profile, docs=docs.sportsmans.update_profile)
url.POST("    /sportsman/profile/avatar             ", endpoint=endpoints.sportsmans.profile.upload_avatar, docs=docs.trainers.upload_avatar)

# Trainer Survey
url.GET("     /trainer/survey                       ", endpoint=endpoints.trainers.surveys.get_survey, docs=docs.trainers.surveys.get_survey)
url.PATCH("   /trainer/survey                       ", endpoint=endpoints.trainers.surveys.update_survey, docs=docs.trainers.surveys.update_survey)
url.GET("     /trainer/survey/sportsman             ", endpoint=endpoints.trainers.surveys.get_sportsman_survey, docs=docs.trainers.surveys.get_sportsman_survey)
url.PATCH("   /trainer/survey/sportsman             ", endpoint=endpoints.trainers.surveys.set_update_sportsman_survey, docs=docs.trainers.surveys.set_update_sportsman_survey)
url.PATCH("   /trainer/survey/team                  ", endpoint=endpoints.trainers.surveys.set_update_team_survey, docs=docs.trainers.surveys.set_update_team_survey)

# Sportsman Survey
url.GET("     /sportsman/survey                     ", endpoint=endpoints.sportsmans.surveys.get_survey, docs=docs.sportsmans.surveys.get_survey)
url.GET("     /sportsman/survey/update              ", endpoint=endpoints.sportsmans.surveys.get_survey_update_flag, docs=docs.sportsmans.surveys.get_survey_update_flag)
url.PATCH("   /sportsman/survey                     ", endpoint=endpoints.sportsmans.surveys.fill_survey, docs=docs.sportsmans.surveys.fill_survey)

# Trainer Team
url.GET("     /trainer/team                         ", endpoint=endpoints.trainers.teams.get_self_team, docs=docs.trainers.get_self_team)

# Sportsman Team
url.GET("     /sportsman/team                       ", endpoint=endpoints.sportsmans.teams.get_self_team, docs=docs.sportsmans.teams.get_self_team)

# Trainer Group
url.GET("     /trainer/groups                       ", endpoint=endpoints.trainers.groups.get_self_groups, docs=docs.trainers.get_self_groups)
url.PATCH("   /trainer/groups                       ", endpoint=endpoints.trainers.groups.update_group, docs=docs.trainers.update_group)
url.DELETE("  /trainer/groups                       ", endpoint=endpoints.trainers.groups.delete_group, docs=docs.trainers.delete_group)
url.POST("    /trainer/groups                       ", endpoint=endpoints.trainers.groups.create_group, docs=docs.trainers.create_group)
url.POST("    /trainer/groups/add                   ", endpoint=endpoints.trainers.groups.add_sportsman_to_group, docs=docs.trainers.add_sportsman_to_group)
url.POST("    /trainer/groups/adds                  ", endpoint=endpoints.trainers.groups.adds_sportsmans_to_group, docs=docs.trainers.adds_sportsmans_to_group)
url.POST("    /trainer/groups/kick                  ", endpoint=endpoints.trainers.groups.kick_sportsman_off_group, docs=docs.trainers.kick_sportsman_off_group)
url.POST("    /trainer/groups/kicks                 ", endpoint=endpoints.trainers.groups.kicks_sportsmans_off_group, docs=docs.trainers.kicks_sportsmans_off_group)

# Sportsman Group
url.GET("     /sportsman/groups                     ", endpoint=endpoints.sportsmans.groups.get_self_groups, docs=docs.sportsmans.get_self_groups)
url.GET("     /sportsman/groups/{id}                ", endpoint=endpoints.sportsmans.groups.get_self_group, docs=docs.sportsmans.get_self_group)
url.POST("    /sportsman/groups/outs                ", endpoint=endpoints.sportsmans.groups.outs_off_groups, docs=docs.sportsmans.outs_off_groups)
url.POST("    /sportsman/groups/out/{id}            ", endpoint=endpoints.sportsmans.groups.out_off_group, docs=docs.sportsmans.out_off_group)

# Trainer Workout
url.GET("     /trainer/workouts/team                ", endpoint=endpoints.trainers.workouts.get_workouts_for_team, docs=docs.trainers.get_workouts_for_team)
url.POST("    /trainer/workouts/team                ", endpoint=endpoints.trainers.workouts.create_workout_for_team, docs=docs.trainers.create_workout_for_team)
url.GET("     /trainer/workouts/group               ", endpoint=endpoints.trainers.workouts.get_workouts_for_group, docs=docs.trainers.get_workouts_for_group)
url.POST("    /trainer/workouts/group               ", endpoint=endpoints.trainers.workouts.create_workout_for_group, docs=docs.trainers.create_workout_for_group)
url.GET("     /trainer/workouts/sportsman           ", endpoint=endpoints.trainers.workouts.get_workouts_for_sportsman, docs=docs.trainers.get_workouts_for_sportsman)
url.POST("    /trainer/workouts/individual          ", endpoint=endpoints.trainers.workouts.create_workout_for_sportsman, docs=docs.trainers.create_workout_for_sportsman)
url.GET("     /trainer/workouts                     ", endpoint=endpoints.trainers.workouts.get_workouts, docs=docs.trainers.get_workouts)
url.GET("     /trainer/workouts/pool                ", endpoint=endpoints.trainers.workouts.get_workouts_by_pool_id, docs=docs.trainers.get_workouts_by_pool_id)
url.PATCH("   /trainer/workouts                     ", endpoint=endpoints.trainers.workouts.update_workout, docs=docs.trainers.update_workout)
url.DELETE("  /trainer/workouts                     ", endpoint=endpoints.trainers.workouts.delete_workout, docs=docs.trainers.delete_workout)

# Trainer Workouts Pool 
url.GET("     /trainer/workouts-pool                ", endpoint=endpoints.trainers.workouts_pool.get_workouts_pool, docs=docs.trainers.get_workouts_pool)
url.POST("    /trainer/workouts-pool                ", endpoint=endpoints.trainers.workouts_pool.create_workout_pool, docs=docs.trainers.create_workout_pool)
url.DELETE("  /trainer/workouts-pool                ", endpoint=endpoints.trainers.workouts_pool.delete_workout_pool, docs=docs.trainers.delete_workout_pool)
url.PATCH("   /trainer/workouts-pool                ", endpoint=endpoints.trainers.workouts_pool.update_workout_pool, docs=docs.trainers.update_workout_pool)

# Sportsman Workouts
url.GET("     /sportsman/workouts/{id}              ", endpoint=endpoints.sportsmans.workouts.get_workout, docs=docs.sportsmans.get_workout)
url.GET("     /sportsman/workouts                   ", endpoint=endpoints.sportsmans.workouts.get_workouts, docs=docs.sportsmans.get_workouts)



urls_router.include_router(endpoints.general.auth.router, tags=[docs.tags_mapper["general_auth"]])
urls_router.include_router(endpoints.general.exercises_types.router, tags=[docs.tags_mapper["general_exercises"]])

urls_router.include_router(endpoints.trainers.auth.router, tags=[docs.tags_mapper["trainers_auth"]])
urls_router.include_router(endpoints.trainers.profile.router, tags=[docs.tags_mapper["trainers_profile"]])
urls_router.include_router(endpoints.trainers.surveys.router, tags=[docs.tags_mapper["trainers_surveys"]])
urls_router.include_router(endpoints.trainers.teams.router, tags=[docs.tags_mapper["trainers_teams"]])
urls_router.include_router(endpoints.trainers.groups.router, tags=[docs.tags_mapper["trainers_groups"]])
urls_router.include_router(endpoints.trainers.workouts.router, tags=[docs.tags_mapper["trainers_workouts"]])
urls_router.include_router(endpoints.trainers.workouts_pool.router, tags=[docs.tags_mapper["trainers_workouts_pool"]])

urls_router.include_router(endpoints.sportsmans.auth.router, tags=[docs.tags_mapper["sportsmans_auth"]])
urls_router.include_router(endpoints.sportsmans.profile.router, tags=[docs.tags_mapper["sportsmans_profile"]])
urls_router.include_router(endpoints.sportsmans.surveys.router, tags=[docs.tags_mapper["sportsmans_surveys"]])
urls_router.include_router(endpoints.sportsmans.teams.router, tags=[docs.tags_mapper["sportsmans_teams"]])
urls_router.include_router(endpoints.sportsmans.groups.router, tags=[docs.tags_mapper["sportsmans_groups"]])
urls_router.include_router(endpoints.sportsmans.workouts.router, tags=[docs.tags_mapper["sportsmans_workouts"]])
