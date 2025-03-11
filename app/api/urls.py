from app.utils.router import EndPointRouter, url

from . import docs, endpoints

urls_router = EndPointRouter()

# General Auth
url.POST("    /auth/login                                        ", endpoint=endpoints.general.login, docs=docs.general.login)
url.POST("    /auth/logout                                       ", endpoint=endpoints.general.logout, docs=docs.general.logout)
url.POST("    /auth/refresh                                      ", endpoint=endpoints.general.refresh, docs=docs.general.refresh)
url.POST("    /auth/verify                                       ", endpoint=endpoints.general.verify, docs=docs.general.verify)

# General Registration
url.POST("    /auth/register                                     ", endpoint=endpoints.general.register, docs=docs.general.register)
url.POST("    /auth/email                                        ", endpoint=endpoints.general.send_confirm_email, docs=docs.general.send_email)
url.POST("    /auth/email/confirm                                ", endpoint=endpoints.general.confirm_email, docs=docs.general.confirm_email)

# General Password reset
url.POST("    /auth/password                                     ", endpoint=endpoints.general.reset_password, docs=docs.general.reset_password)
url.POST("    /auth/password/send                                ", endpoint=endpoints.general.send_confirm_password, docs=docs.general.send_confirm_password)
url.POST("    /auth/password/confirm                             ", endpoint=endpoints.general.confirm_password, docs=docs.general.confirm_password)

# General Exercises Types
url.GET("     /exercises/types                                   ", endpoint=endpoints.general.get_exercises_types, docs=docs.general.get_exercises_types)

# General Workouts Statuses
url.GET("     /workouts/statuses                                 ", endpoint=endpoints.general.get_workouts_statuses, docs=docs.general.get_workouts_statuses)

# Trainer Register
# url.POST("    /trainer/register                                  ", endpoint=endpoints.trainers.register_trainer, docs=docs.trainers.register_trainer)
# url.POST("    /trainer/email                                     ", endpoint=endpoints.trainers.send_confirm_trainer_email, docs=docs.trainers.send_confirm_trainer_email)
# url.POST("    /trainer/email/confirm                             ", endpoint=endpoints.trainers.confirm_trainer_email, docs=docs.trainers.confirm_trainer_email)

# Sportsman Register
# url.POST("    /sportsman/register                                ", endpoint=endpoints.sportsmans.register_sportsman, docs=docs.sportsmans.register_sportsman)
# url.POST("    /sportsman/email                                   ", endpoint=endpoints.sportsmans.send_confirm_sportsman_email, docs=docs.sportsmans.send_confirm_sportsman_email)
# url.POST("    /sportsman/email/confirm                           ", endpoint=endpoints.sportsmans.confirm_sportsman_email, docs=docs.sportsmans.confirm_sportsman_email)

# Trainer Profile
url.GET("     /trainer/profile                                   ", endpoint=endpoints.trainers.get_profile, docs=docs.trainers.get_profile)
url.PATCH("   /trainer/profile                                   ", endpoint=endpoints.trainers.update_profile, docs=docs.trainers.update_profile)
url.POST("    /trainer/profile/avatar                            ", endpoint=endpoints.trainers.upload_avatar, docs=docs.trainers.upload_avatar)

# Sportsman Profile
url.GET("     /sportsman/profile                                 ", endpoint=endpoints.sportsmans.get_profile, docs=docs.sportsmans.get_profile)
url.PATCH("   /sportsman/profile                                 ", endpoint=endpoints.sportsmans.update_profile, docs=docs.sportsmans.update_profile)
url.POST("    /sportsman/profile/avatar                          ", endpoint=endpoints.sportsmans.upload_avatar, docs=docs.trainers.upload_avatar)

# Trainer Survey
url.GET("     /trainer/survey                                    ", endpoint=endpoints.trainers.get_survey, docs=docs.trainers.get_survey)
url.PATCH("   /trainer/survey                                    ", endpoint=endpoints.trainers.update_survey, docs=docs.trainers.update_survey)
url.GET("     /trainer/survey/sportsman                          ", endpoint=endpoints.trainers.get_sportsman_survey, docs=docs.trainers.get_sportsman_survey)
url.PATCH("   /trainer/survey/sportsman                          ", endpoint=endpoints.trainers.set_update_sportsman_survey, docs=docs.trainers.set_update_sportsman_survey)
url.POST("    /trainer/survey/sportsman                          ", endpoint=endpoints.trainers.fill_survey_for_sportsman, docs=docs.trainers.fill_survey_for_sportsman)
url.PATCH("   /trainer/survey/team                               ", endpoint=endpoints.trainers.set_update_team_survey, docs=docs.trainers.set_update_team_survey)

# Sportsman Survey
url.GET("     /sportsman/survey                                  ", endpoint=endpoints.sportsmans.get_survey, docs=docs.sportsmans.get_survey)
url.GET("     /sportsman/survey/update                           ", endpoint=endpoints.sportsmans.get_survey_update_flag, docs=docs.sportsmans.get_survey_update_flag)
url.PATCH("   /sportsman/survey                                  ", endpoint=endpoints.sportsmans.fill_survey, docs=docs.sportsmans.fill_survey)

# Trainer Team
url.GET("     /trainer/team                                      ", endpoint=endpoints.trainers.get_self_team, docs=docs.trainers.get_self_team)
url.PATCH("   /trainer/team                                      ", endpoint=endpoints.trainers.update_team_name)

# Sportsman Team
url.GET("     /sportsman/team                                    ", endpoint=endpoints.sportsmans.get_self_team, docs=docs.sportsmans.teams.get_self_team)

# Trainer Group
url.GET("     /trainer/groups                                    ", endpoint=endpoints.trainers.get_self_groups, docs=docs.trainers.get_self_groups)
url.PATCH("   /trainer/groups                                    ", endpoint=endpoints.trainers.update_group, docs=docs.trainers.update_group)
url.DELETE("  /trainer/groups                                    ", endpoint=endpoints.trainers.delete_group, docs=docs.trainers.delete_group)
url.POST("    /trainer/groups                                    ", endpoint=endpoints.trainers.create_group, docs=docs.trainers.create_group)
url.POST("    /trainer/groups/add                                ", endpoint=endpoints.trainers.add_sportsman_to_group, docs=docs.trainers.add_sportsman_to_group)
url.POST("    /trainer/groups/adds                               ", endpoint=endpoints.trainers.adds_sportsmans_to_group, docs=docs.trainers.adds_sportsmans_to_group)
url.POST("    /trainer/groups/kick                               ", endpoint=endpoints.trainers.kick_sportsman_off_group, docs=docs.trainers.kick_sportsman_off_group)
url.POST("    /trainer/groups/kicks                              ", endpoint=endpoints.trainers.kicks_sportsmans_off_group, docs=docs.trainers.kicks_sportsmans_off_group)

# Sportsman Group
url.GET("     /sportsman/groups                                  ", endpoint=endpoints.sportsmans.get_self_groups, docs=docs.sportsmans.get_self_groups)
url.GET("     /sportsman/groups/{id}                             ", endpoint=endpoints.sportsmans.get_self_group, docs=docs.sportsmans.get_self_group)
url.POST("    /sportsman/groups/outs                             ", endpoint=endpoints.sportsmans.outs_off_groups, docs=docs.sportsmans.outs_off_groups)
url.POST("    /sportsman/groups/out/{id}                         ", endpoint=endpoints.sportsmans.out_off_group, docs=docs.sportsmans.out_off_group)

# Trainer Exercise Type
url.POST("     /trainer/exercises                                ", endpoint=endpoints.trainers.create_exercise_type, docs=docs.trainers.create_exercise_type)
url.PATCH("    /trainer/exercises                                ", endpoint=endpoints.trainers.update_exercise_type, docs=docs.trainers.update_exercise_type)
url.DELETE("   /trainer/exercises                                ", endpoint=endpoints.trainers.delete_exercise_type, docs=docs.trainers.delete_exercise_type)
url.POST("     /trainer/exercises/reset                          ", endpoint=endpoints.trainers.reset_exercises_types, docs=docs.trainers.reset_exercises_types)

# Trainer Workout
url.GET("     /trainer/workouts/team                             ", endpoint=endpoints.trainers.get_workouts_for_team, docs=docs.trainers.get_workouts_for_team)
url.POST("    /trainer/workouts/team                             ", endpoint=endpoints.trainers.create_workout_for_team, docs=docs.trainers.create_workout_for_team)
url.POST("    /trainer/workouts/team/repeat                      ", endpoint=endpoints.trainers.repeat_workout_for_team)
url.GET("     /trainer/workouts/group                            ", endpoint=endpoints.trainers.get_workouts_for_group, docs=docs.trainers.get_workouts_for_group)
url.POST("    /trainer/workouts/group                            ", endpoint=endpoints.trainers.create_workout_for_group, docs=docs.trainers.create_workout_for_group)
url.POST("    /trainer/workouts/group/repeat                     ", endpoint=endpoints.trainers.create_workout_for_group)
url.GET("     /trainer/workouts/sportsman                        ", endpoint=endpoints.trainers.get_workouts_for_sportsman, docs=docs.trainers.get_workouts_for_sportsman)
url.POST("    /trainer/workouts/individual                       ", endpoint=endpoints.trainers.create_workout_for_sportsman, docs=docs.trainers.create_workout_for_sportsman)
url.POST("    /trainer/workouts/individual/repeat                ", endpoint=endpoints.trainers.create_workout_for_sportsman)
url.GET("     /trainer/workouts                                  ", endpoint=endpoints.trainers.get_workouts, docs=docs.trainers.get_workouts)
url.GET("     /trainer/workouts/pool                             ", endpoint=endpoints.trainers.get_workouts_by_pool_id, docs=docs.trainers.get_workouts_by_pool_id)
url.PATCH("   /trainer/workouts                                  ", endpoint=endpoints.trainers.update_workout, docs=docs.trainers.update_workout)
url.DELETE("  /trainer/workouts                                  ", endpoint=endpoints.trainers.delete_workout, docs=docs.trainers.delete_workout)
url.DELETE("  /trainer/workouts/repeat                           ", endpoint=endpoints.trainers.delete_repeat_workout)

# Trainer Workouts Pool 
url.GET("     /trainer/workouts-pool                             ", endpoint=endpoints.trainers.get_workouts_pool, docs=docs.trainers.get_workouts_pool)
url.POST("    /trainer/workouts-pool                             ", endpoint=endpoints.trainers.create_workout_pool, docs=docs.trainers.create_workout_pool)
url.DELETE("  /trainer/workouts-pool                             ", endpoint=endpoints.trainers.delete_workout_pool, docs=docs.trainers.delete_workout_pool)
url.PATCH("   /trainer/workouts-pool                             ", endpoint=endpoints.trainers.update_workout_pool, docs=docs.trainers.update_workout_pool)

# Sportsman Workouts
url.GET("     /sportsman/workouts/{id}                           ", endpoint=endpoints.sportsmans.get_workout, docs=docs.sportsmans.get_workout)
url.GET("     /sportsman/workouts                                ", endpoint=endpoints.sportsmans.get_workouts, docs=docs.sportsmans.get_workouts)

url.PATCH("   /trainer/workouts/start                            ", endpoint=endpoints.trainers.start_workout, docs=docs.trainers.start_workout)
url.PATCH("   /trainer/workouts/sportsmans/start                 ", endpoint=endpoints.trainers.start_workout_for_sportsmans, docs=docs.trainers.start_workout_for_sportsmans)
url.PATCH("   /trainer/workouts/complete                         ", endpoint=endpoints.trainers.complete_workout, docs=docs.trainers.complete_workout)
url.PATCH("   /trainer/workouts/sportsmans/complete              ", endpoint=endpoints.trainers.complete_workout_for_sportsmans, docs=docs.trainers.complete_workout_for_sportsmans)
url.PATCH("   /trainer/workouts/cancel                           ", endpoint=endpoints.trainers.cancel_workout, docs=docs.trainers.cancel_workout)
url.PATCH("   /trainer/workouts/sportsmans/cancel                ", endpoint=endpoints.trainers.cancel_workout_for_sportsmans, docs=docs.trainers.cancel_workout_for_sportsmans)
url.PATCH("   /trainer/workouts/statuses                         ", endpoint=endpoints.trainers.get_workout_statuses, docs=docs.trainers.get_workout_statuses)

# Sportsman Workouts Management
url.PATCH("   /sportsman/workouts/{id}/start                     ", endpoint=endpoints.sportsmans.start_workout, docs=docs.sportsmans.start_workout)
url.PATCH("   /sportsman/workouts/{id}/complete                  ", endpoint=endpoints.sportsmans.complete_workout, docs=docs.sportsmans.complete_workout)
url.PATCH("   /sportsman/workouts/{id}/cancel                    ", endpoint=endpoints.sportsmans.cancel_workout, docs=docs.sportsmans.cancel_workout)

# Trainer Stress Questionnaires
url.GET("     /trainer/stress-questions/sportsman                ", endpoint=endpoints.trainers.get_all_stress_questionnaires_by_sportsman, docs=docs.trainers.get_all_stress_questionnaires_by_sportsman)
url.GET("     /trainer/stress-questions/workout                  ", endpoint=endpoints.trainers.get_all_stress_questionnaires_by_workout, docs=docs.trainers.get_all_stress_questionnaires_by_workout)
url.GET("     /trainer/stress-questions                          ", endpoint=endpoints.trainers.get_stress_questionnaire, docs=docs.trainers.get_stress_questionnaire)

# Sportsman Stress Questionnaires
url.GET("     /sportsman/stress-questions/active                 ", endpoint=endpoints.sportsmans.get_active_stress_questionnaires, docs=docs.sportsmans.get_active_stress_questionnaires)
url.GET("     /sportsman/stress-questions                        ", endpoint=endpoints.sportsmans.get_all_stress_questionnaires, docs=docs.sportsmans.get_all_stress_questionnaires)
url.GET("     /sportsman/stress-questions/{id}                   ", endpoint=endpoints.sportsmans.get_stress_questionnaire, docs=docs.sportsmans.get_stress_questionnaire)
url.GET("     /sportsman/stress-questions/workout/{workout_id}   ", endpoint=endpoints.sportsmans.get_stress_questionnaire_by_workout_id, docs=docs.sportsmans.get_stress_questionnaire_by_workout_id)
url.PATCH("   /sportsman/stress-questions/{id}                   ", endpoint=endpoints.sportsmans.fill_stress_questionnaire, docs=docs.sportsmans.fill_stress_questionnaire)

# Trainer Health Questionnaires
url.GET("     /trainer/health-questions/sportsman                ", endpoint=endpoints.trainers.get_all_health_questionnaires_by_sportsman, docs=docs.trainers.get_all_health_questionnaires_by_sportsman)
url.GET("     /trainer/health-questions                          ", endpoint=endpoints.trainers.get_health_questionnaire, docs=docs.trainers.get_health_questionnaire)

# Sportsman Health Questionnaires
url.GET("     /sportsman/health-questions/active                 ", endpoint=endpoints.sportsmans.get_active_health_questionnaire, docs=docs.sportsmans.get_active_health_questionnaire)
url.GET("     /sportsman/health-questions                        ", endpoint=endpoints.sportsmans.get_all_health_questionnaires, docs=docs.sportsmans.get_all_health_questionnaires)
url.GET("     /sportsman/health-questions/{id}                   ", endpoint=endpoints.sportsmans.get_health_questionnaire, docs=docs.sportsmans.get_health_questionnaire)
url.PATCH("   /sportsman/health-questions/{id}                   ", endpoint=endpoints.sportsmans.fill_health_questionnaire, docs=docs.sportsmans.fill_health_questionnaire)


# General
urls_router.include_router(endpoints.general.auth.router, tags=[docs.tags_mapper["general_auth"]])
urls_router.include_router(endpoints.general.registration.router, tags=[docs.tags_mapper["general_registration"]])
urls_router.include_router(endpoints.general.password.router, tags=[docs.tags_mapper["general_password"]])
urls_router.include_router(endpoints.general.exercises_types.router, tags=[docs.tags_mapper["general_exercises"]])
urls_router.include_router(endpoints.general.workouts_statuses.router, tags=[docs.tags_mapper["general_workouts_statuses"]])

# Trainer
# urls_router.include_router(endpoints.trainers.auth.router, tags=[docs.tags_mapper["trainers_auth"]])
urls_router.include_router(endpoints.trainers.profile.router, tags=[docs.tags_mapper["trainers_profile"]])
urls_router.include_router(endpoints.trainers.surveys.router, tags=[docs.tags_mapper["trainers_surveys"]])
urls_router.include_router(endpoints.trainers.teams.router, tags=[docs.tags_mapper["trainers_teams"]])
urls_router.include_router(endpoints.trainers.groups.router, tags=[docs.tags_mapper["trainers_groups"]])
urls_router.include_router(endpoints.trainers.exercises_types.router, tags=[docs.tags_mapper["trainers_exercises"]])
urls_router.include_router(endpoints.trainers.workouts.router, tags=[docs.tags_mapper["trainers_workouts"]])
urls_router.include_router(endpoints.trainers.workouts_management.router, tags=[docs.tags_mapper["trainers_workouts_management"]])
urls_router.include_router(endpoints.trainers.workouts_pool.router, tags=[docs.tags_mapper["trainers_workouts_pool"]])
urls_router.include_router(endpoints.trainers.stress_questionnaires.router, tags=[docs.tags_mapper["trainers_stress_questionnaires"]])
urls_router.include_router(endpoints.trainers.health_questionnaires.router, tags=[docs.tags_mapper["trainers_health_questionnaires"]])

# Sportsman
# urls_router.include_router(endpoints.sportsmans.auth.router, tags=[docs.tags_mapper["sportsmans_auth"]])
urls_router.include_router(endpoints.sportsmans.profile.router, tags=[docs.tags_mapper["sportsmans_profile"]])
urls_router.include_router(endpoints.sportsmans.surveys.router, tags=[docs.tags_mapper["sportsmans_surveys"]])
urls_router.include_router(endpoints.sportsmans.teams.router, tags=[docs.tags_mapper["sportsmans_teams"]])
urls_router.include_router(endpoints.sportsmans.groups.router, tags=[docs.tags_mapper["sportsmans_groups"]])
urls_router.include_router(endpoints.sportsmans.workouts.router, tags=[docs.tags_mapper["sportsmans_workouts"]])
urls_router.include_router(endpoints.sportsmans.workouts_management.router, tags=[docs.tags_mapper["sportsmans_workouts_management"]])
urls_router.include_router(endpoints.sportsmans.stress_questionnaires.router, tags=[docs.tags_mapper["sportsmans_stress_questionnaires"]])
urls_router.include_router(endpoints.sportsmans.health_questionnaires.router, tags=[docs.tags_mapper["sportsmans_health_questionnaires"]])
