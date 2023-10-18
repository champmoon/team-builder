from app.utils.router import EndPointRouter, url

from . import docs
from .endpoints import trainers_auth
from .endpoints import sportsmans_auth

urls_router = EndPointRouter()


url.POST("    /trainers/register                    ", endpoint=trainers_auth.register)
url.POST("    /trainers/login                       ", endpoint=trainers_auth.login)
url.POST("    /trainers/logout                      ", endpoint=trainers_auth.logout)
url.POST("    /trainers/refresh                     ", endpoint=trainers_auth.refresh)
url.POST("    /trainers/verify                      ", endpoint=trainers_auth.verify)

url.POST("    /sportsmans/register                  ", endpoint=sportsmans_auth.register)
url.POST("    /sportsmans/login                     ", endpoint=sportsmans_auth.login)
url.POST("    /sportsmans/logout                    ", endpoint=sportsmans_auth.logout)
url.POST("    /sportsmans/refresh                   ", endpoint=sportsmans_auth.refresh)
url.POST("    /sportsmans/verify                    ", endpoint=sportsmans_auth.verify)

urls_router.include_router(trainers_auth.router, tags=[docs.tags_mapper["trainers_auth"]])
urls_router.include_router(sportsmans_auth.router, tags=[docs.tags_mapper["sportsmans_auth"]])
