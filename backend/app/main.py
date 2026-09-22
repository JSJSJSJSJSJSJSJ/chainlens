"""Application entry point: uvicorn app.main:app."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.engine import Engine

from app.api.exception_handlers import register_exception_handlers
from app.api.router import api_router
from app.core.config import snapshot_path
from app.db.session import make_engine
from app.services.import_service import ensure_dataset


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

    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
