from app.utils.router import EndPointRouter, url

from . import docs
from .endpoints import auth

urls_router = EndPointRouter()


url.POST("    /auth/register         ", endpoint=auth.register, docs=docs.register)
url.POST("    /auth/login            ", endpoint=auth.login, docs=docs.login)
url.POST("    /auth/logout           ", endpoint=auth.logout, docs=docs.logout)
url.POST("    /auth/refresh          ", endpoint=auth.refresh, docs=docs.refresh)
url.POST("    /auth/verify           ", endpoint=auth.verify, docs=docs.verify)

urls_router.include_router(auth.router, tags=[docs.tags_mapper["auth"]])
