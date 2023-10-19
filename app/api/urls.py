from app.utils.router import EndPointRouter, url

from . import docs
from .endpoints import trainers_auth
from .endpoints import sportsmans_auth

urls_router = EndPointRouter()


url.POST("    /trainers/register         ", endpoint=trainers_auth.register, docs=docs.trainer_register)
url.POST("    /trainers/login            ", endpoint=trainers_auth.login, docs=docs.trainer_login)
url.POST("    /trainers/logout           ", endpoint=trainers_auth.logout, docs=docs.trainer_logout)
url.POST("    /trainers/refresh          ", endpoint=trainers_auth.refresh, docs=docs.trainer_refresh)
url.POST("    /trainers/verify           ", endpoint=trainers_auth.verify, docs=docs.trainer_verify)

url.POST("    /sportsmans/register       ", endpoint=sportsmans_auth.register, docs=docs.sportsman_register)
url.POST("    /sportsmans/login          ", endpoint=sportsmans_auth.login, docs=docs.sportsman_register)
url.POST("    /sportsmans/logout         ", endpoint=sportsmans_auth.logout, docs=docs.sportsman_register)
url.POST("    /sportsmans/refresh        ", endpoint=sportsmans_auth.refresh, docs=docs.sportsman_register)
url.POST("    /sportsmans/verify         ", endpoint=sportsmans_auth.verify, docs=docs.sportsman_register)

urls_router.include_router(trainers_auth.router, tags=[docs.tags_mapper["trainers_auth"]])
urls_router.include_router(sportsmans_auth.router, tags=[docs.tags_mapper["sportsmans_auth"]])
