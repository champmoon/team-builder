from app.utils.router import EndPointRouter, url

from . import docs
from .endpoints import general

from .endpoints.trainers import (
    teams as trainers_teams,
    groups as trainers_groups,
    profile as trainers_profile,
    workouts as trainers_workouts,
)
from .endpoints.sportsmans import (
    teams as sportsmans_teams,
    groups as sportsmans_groups,
    profile as sportsmans_profile,
)

urls_router = EndPointRouter()


url.POST("    /auth/register                        ", endpoint=general.auth.register, docs=docs.register)
url.POST("    /auth/login                           ", endpoint=general.auth.login, docs=docs.login)
url.POST("    /auth/logout                          ", endpoint=general.auth.logout, docs=docs.logout)
url.POST("    /auth/refresh                         ", endpoint=general.auth.refresh, docs=docs.refresh)
url.POST("    /auth/verify                          ", endpoint=general.auth.verify, docs=docs.verify)

url.GET("     /trainer/profile                      ", endpoint=trainers_profile.get_profile, docs=docs.trainers.get_profile)
url.PATCH("   /trainer/profile                      ", endpoint=trainers_profile.update_profile, docs=docs.trainers.update_profile)

url.GET("     /sportsman/profile                    ", endpoint=sportsmans_profile.get_profile, docs=docs.sportsmans.get_profile)
url.PATCH("   /sportsman/profile                    ", endpoint=sportsmans_profile.update_profile, docs=docs.sportsmans.update_profile)

url.GET("     /trainer/team                         ", endpoint=trainers_teams.get_self_team, docs=docs.trainers.get_self_team)
url.POST("    /trainer/team/add                     ", endpoint=trainers_teams.add_sportsman_to_team, docs=docs.trainers.add_sportsman_to_team)
url.POST("    /trainer/team/adds                    ", endpoint=trainers_teams.adds_sportsmans_to_team, docs=docs.trainers.adds_sportsmans_to_team)
url.POST("    /trainer/team/kick                    ", endpoint=trainers_teams.kick_sportsman_off_team, docs=docs.trainers.kick_sportsman_off_team)
url.POST("    /trainer/team/kicks                   ", endpoint=trainers_teams.kicks_sportsmans_off_team, docs=docs.trainers.kicks_sportsmans_off_team)

url.GET("     /sportsman/team                       ", endpoint=sportsmans_teams.get_self_team, docs=docs.sportsmans.teams.get_self_team)
url.POST("    /sportsman/team/out                   ", endpoint=sportsmans_teams.out_off_team, docs=docs.sportsmans.teams.out_off_team)

url.GET("     /trainer/groups                       ", endpoint=trainers_groups.get_self_groups, docs=docs.trainers.get_self_groups)
url.GET("     /trainer/groups/{id}                  ", endpoint=trainers_groups.get_self_group, docs=docs.trainers.get_self_group)
url.PATCH("   /trainer/groups/{id}                  ", endpoint=trainers_groups.update_group, docs=docs.trainers.update_group)
url.DELETE("  /trainer/groups/{id}                  ", endpoint=trainers_groups.delete_group, docs=docs.trainers.delete_group)
url.POST("    /trainer/groups                       ", endpoint=trainers_groups.create_group, docs=docs.trainers.create_group)
url.POST("    /trainer/groups/add                   ", endpoint=trainers_groups.add_sportsman_to_group, docs=docs.trainers.add_sportsman_to_group)
url.POST("    /trainer/groups/adds                  ", endpoint=trainers_groups.adds_sportsmans_to_group, docs=docs.trainers.adds_sportsmans_to_group)
url.POST("    /trainer/groups/kick                  ", endpoint=trainers_groups.kick_sportsman_off_group, docs=docs.trainers.kick_sportsman_off_group)
url.POST("    /trainer/groups/kicks                 ", endpoint=trainers_groups.kicks_sportsmans_off_group, docs=docs.trainers.kicks_sportsmans_off_group)

url.GET("     /sportsman/groups                     ", endpoint=sportsmans_groups.get_self_groups, docs=docs.sportsmans.get_self_groups)
url.GET("     /sportsman/groups/{id}                ", endpoint=sportsmans_groups.get_self_group, docs=docs.sportsmans.get_self_group)
url.POST("    /sportsman/groups/outs                ", endpoint=sportsmans_groups.outs_off_groups, docs=docs.sportsmans.outs_off_groups)
url.POST("    /sportsman/groups/out/{id}            ", endpoint=sportsmans_groups.out_off_group, docs=docs.sportsmans.out_off_group)

url.GET("     /exercises/types                      ", endpoint=general.exercises_types.get_exercises_types)

url.POST("    /trainer/workout/sportsman            ", endpoint=trainers_workouts.create_workout_for_sportsman)
url.GET("     /trainer/workout/sportsman/{email}    ", endpoint=trainers_workouts.get_workouts_for_sportsman)
url.POST("    /trainer/workout/group                ", endpoint=trainers_workouts.create_workout_for_group)
url.GET("     /trainer/workout/group/{id}           ", endpoint=trainers_workouts.get_workouts_for_group)
url.POST("    /trainer/workout/team                 ", endpoint=trainers_workouts.create_workout_for_team)
url.GET("     /trainer/workout/team                 ", endpoint=trainers_workouts.get_workouts_for_team)
url.GET("     /trainer/workouts                     ", endpoint=trainers_workouts.get_workouts)
url.GET("     /trainer/workouts/{id}                ", endpoint=trainers_workouts.get_workout)
url.DELETE("  /trainer/workouts/{id}                ", endpoint=trainers_workouts.delete_workout)


urls_router.include_router(general.auth.router, tags=[docs.tags_mapper["auth"]])

urls_router.include_router(trainers_profile.router, tags=[docs.tags_mapper["trainers_profile"]])
urls_router.include_router(sportsmans_profile.router, tags=[docs.tags_mapper["sportsmans_profile"]])

urls_router.include_router(trainers_teams.router, tags=[docs.tags_mapper["trainers_teams"]])
urls_router.include_router(sportsmans_teams.router, tags=[docs.tags_mapper["sportsmans_teams"]])

urls_router.include_router(trainers_groups.router, tags=[docs.tags_mapper["trainers_groups"]])
urls_router.include_router(sportsmans_groups.router, tags=[docs.tags_mapper["sportsmans_groups"]])

urls_router.include_router(general.exercises_types.router, tags=[docs.tags_mapper["exercises"]])


urls_router.include_router(trainers_workouts.router, tags=[docs.tags_mapper["trainers_workouts"]])

