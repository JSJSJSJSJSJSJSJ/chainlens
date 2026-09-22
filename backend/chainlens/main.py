"""Run with uvicorn chainlens.main:app --host 127.0.0.1 --port 8000."""

import logging
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from .config import snapshot_path
from .database import make_engine
from .errors import DomainError
from .importer import ensure_dataset
from .schemas import QueryFilters
from .service import ResearchService


def create_app(
    engine: Engine | None = None, snapshot: Path | None = None, auto_import=True
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.engine = engine if engine is not None else make_engine()
        if auto_import:
            ensure_dataset(app.state.engine, snapshot or snapshot_path())
        yield
        if engine is None:
            app.state.engine.dispose()

    app = FastAPI(title="ChainLens 链鉴", version="0.1.0", lifespan=lifespan)

    @app.exception_handler(DomainError)
    async def domain_error(_request: Request, exc: DomainError):
        return JSONResponse(status_code=exc.status, content=jsonable_encoder(exc.payload()))

    @app.exception_handler(RequestValidationError)
    async def invalid_request(_request: Request, exc: RequestValidationError):
        details = [
            {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "查询参数格式或范围不正确",
                    "details": details,
                }
            },
        )

    @app.exception_handler(HTTPException)
    async def http_error(_request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR",
                    "message": str(exc.detail),
                    "details": [],
                }
            },
        )

    @app.exception_handler(Exception)
    async def unexpected_error(_request: Request, exc: Exception):
        logging.getLogger("chainlens").exception("Unexpected request failure", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "服务暂时无法完成请求，请检查服务日志",
                    "details": [],
                }
            },
        )

    def service(request: Request):
        with Session(request.app.state.engine) as session:
            yield ResearchService(session)

    Service = Annotated[ResearchService, Depends(service)]
    Filters = Annotated[QueryFilters, Query()]

    @app.get("/api/health")
    def health(svc: Service):
        return svc.health()

    @app.get("/api/companies")
    def companies(
        svc: Service,
        q: Annotated[str | None, Query(max_length=200)] = None,
        page: Annotated[int, Query(ge=1)] = 1,
        page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    ):
        return svc.companies(q, page, page_size)

    @app.get("/api/companies/{company_id}")
    def company(company_id: str, svc: Service):
        return svc.company(company_id)

    @app.get("/api/companies/{company_id}/relationships")
    def relationships(company_id: str, filters: Filters, svc: Service):
        return svc.relationships(company_id, filters)

    @app.get("/api/companies/{company_id}/graph")
    def graph(company_id: str, filters: Filters, svc: Service):
        return svc.graph(company_id, filters)

    @app.get("/api/relationships/{relationship_id}")
    def relationship(relationship_id: str, svc: Service, known_at: date | None = None):
        return svc.relationship(relationship_id, known_at)

    @app.get("/api/relationships/{relationship_id}/evidence")
    def evidence(relationship_id: str, svc: Service, known_at: date | None = None):
        return svc.evidence(relationship_id, known_at)

    return app


app = create_app()
