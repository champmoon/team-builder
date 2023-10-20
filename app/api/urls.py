from app.utils.router import EndPointRouter, url

from . import docs
from .endpoints import auth

from .endpoints.trainers import (
    teams as trainers_teams,
    groups as groups_teams
)
from .endpoints.sportsmans import (
    teams as sportsmans_teams
)

urls_router = EndPointRouter()


url.POST("   /auth/register                           ", endpoint=auth.register, docs=docs.register)
url.POST("   /auth/login                              ", endpoint=auth.login, docs=docs.login)
url.POST("   /auth/logout                             ", endpoint=auth.logout, docs=docs.logout)
url.POST("   /auth/refresh                            ", endpoint=auth.refresh, docs=docs.refresh)
url.POST("   /auth/verify                             ", endpoint=auth.verify, docs=docs.verify)

url.GET("    /trainer/team                            ", endpoint=trainers_teams.get_self_team)
url.POST("   /trainer/team/add/                       ", endpoint=trainers_teams.add_sportsman_to_team)
url.POST("   /trainer/team/adds                       ", endpoint=trainers_teams.adds_sportsmans_to_team)
url.POST("   /trainer/team/kick/                      ", endpoint=trainers_teams.kick_sportsman_off_team)
url.POST("   /trainer/team/kicks                      ", endpoint=trainers_teams.kicks_sportsmans_off_team)

url.GET("    /trainer/groups                          ", endpoint=groups_teams.get_self_groups)
url.POST("   /trainer/groups                          ", endpoint=groups_teams.create_group)
url.POST("   /trainer/groups/add                      ", endpoint=groups_teams.adds_sportsman_to_group)
url.POST("   /trainer/groups/adds                     ", endpoint=groups_teams.adds_sportsmans_to_group)

url.GET("    /sportsman/team                          ", endpoint=sportsmans_teams.get_self_team)
url.POST("   /sportsman/team/out                      ", endpoint=sportsmans_teams.out_off_team)


urls_router.include_router(auth.router, tags=[docs.tags_mapper["auth"]])

urls_router.include_router(trainers_teams.router, tags=[docs.tags_mapper["trainers_teams"]])
urls_router.include_router(groups_teams.router, tags=[docs.tags_mapper["trainers_groups"]])

urls_router.include_router(sportsmans_teams.router, tags=[docs.tags_mapper["sportsmans_teams"]])
