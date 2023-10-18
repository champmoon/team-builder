from enum import Enum
from typing import Any, Callable, Sequence, Type

from fastapi import APIRouter, params
from fastapi.datastructures import Default
from fastapi.routing import APIRoute
from fastapi.types import DecoratedCallable, IncEx
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.routing import Mount as Mount

from app.api.docs import Docs


class NotSupportedException(Exception):
    def __init__(self) -> None:
        self.msg = (
            "This functionality is not supported in the class - EndPointRouter"
            "use instead - APIRouter from FastAPI"
        )
        super().__init__(self.msg)


class EndPointRouter(APIRouter):
    def endpoint_route(
        self,
        *,
        response_model: Any = Default(...),
        status_code: int | None = None,
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[params.Depends] | None = None,
        summary: str | None = None,
        description: str | None = None,
        response_description: str = "Successful Response",
        responses: dict[int | str, dict[str, Any]] | None = None,
        deprecated: bool | None = None,
        operation_id: str | None = None,
        response_model_include: IncEx | None = None,
        response_model_exclude: IncEx | None = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: str | None = None,
        callbacks: list[BaseRoute] | None = None,
        openapi_extra: dict[str, Any] | None = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[
        [DecoratedCallable], Callable[[str, list[str], Docs], DecoratedCallable]
    ]:
        def decorator(
            func: DecoratedCallable,
        ) -> Callable[[str, list[str], Docs], DecoratedCallable]:
            def url_helper_decorator(
                path: str,
                methods: list[str],
                docs: Docs | None = None,
            ) -> DecoratedCallable:
                self.add_api_route(
                    path,
                    func,
                    response_model=response_model,
                    status_code=status_code,
                    tags=tags,
                    dependencies=dependencies,
                    summary=(
                        docs.get("summary") or summary  # type: ignore
                        if docs
                        else summary
                    ),
                    description=(
                        docs.get("description") or description  # type: ignore
                        if docs
                        else description
                    ),
                    response_description=response_description,
                    responses=(
                        docs.get("responses") or responses  # type: ignore
                        if docs
                        else responses
                    ),
                    deprecated=deprecated,
                    methods=methods,
                    operation_id=operation_id,
                    response_model_include=response_model_include,
                    response_model_exclude=response_model_exclude,
                    response_model_by_alias=response_model_by_alias,
                    response_model_exclude_unset=response_model_exclude_unset,
                    response_model_exclude_defaults=response_model_exclude_defaults,
                    response_model_exclude_none=response_model_exclude_none,
                    include_in_schema=include_in_schema,
                    response_class=response_class,
                    name=name,
                    callbacks=callbacks,
                    openapi_extra=openapi_extra,
                    generate_unique_id_function=generate_unique_id_function,
                )
                return func

            return url_helper_decorator

        return decorator

    def __call__(  # type: ignore
        self,
        *,
        response_model: Any = Default(...),
        status_code: int | None = None,
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[params.Depends] | None = None,
        summary: str | None = None,
        description: str | None = None,
        response_description: str = "Successful Response",
        responses: dict[int | str, dict[str, Any]] | None = None,
        deprecated: bool | None = None,
        operation_id: str | None = None,
        response_model_include: IncEx | None = None,
        response_model_exclude: IncEx | None = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = True,  # Always exclude none for response
        include_in_schema: bool = True,
        response_class: Type[Response] = Default(JSONResponse),
        name: str | None = None,
        callbacks: list[BaseRoute] | None = None,
        openapi_extra: dict[str, Any] | None = None,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> Callable[
        [DecoratedCallable], Callable[[str, list[str], Docs], DecoratedCallable]
    ]:
        return self.endpoint_route(
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def get(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException

    def put(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException

    def post(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException

    def delete(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException

    def options(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException

    def head(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException

    def patch(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException

    def trace(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        raise NotSupportedException


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
