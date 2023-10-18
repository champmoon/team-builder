from typing import Any, Callable

from starlette.routing import Mount as Mount

from app.api.docs import Docs


class url:
    """
    This class is ONLY user for EndPointRouter
    """

    @classmethod
    def GET(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["GET"], docs)

    @classmethod
    def PUT(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["PUT"], docs)

    @classmethod
    def POST(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["POST"], docs)

    @classmethod
    def DELETE(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["DELETE"], docs)

    @classmethod
    def OPTIONS(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["OPTIONS"], docs)

    @classmethod
    def HEAD(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["HEAD"], docs)

    @classmethod
    def PATCH(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["PATCH"], docs)

    @classmethod
    def TRACE(cls, path: str, *, endpoint: Callable, docs: Docs | None = None) -> Any:
        return endpoint(path.strip(), ["PATCH"], docs)
