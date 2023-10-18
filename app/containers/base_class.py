from dependency_injector import containers, providers

from app.cache.connection import Cache
from app.db.session import DB


class BaseContainer(containers.DeclarativeContainer):
    wire_config = "app.api"

    session_factory = providers.Singleton(DB)
    connection_factory = providers.Singleton(Cache)
