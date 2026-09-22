from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401  -- register all tables before create_all
from app.core.config import database_url
from app.db.base import Base


def make_engine(url: str | None = None) -> Engine:
    url = url or database_url()
    parsed = make_url(url)
    kwargs = {}
    if parsed.get_backend_name() == "sqlite":
        kwargs["connect_args"] = {"check_same_thread": False, "timeout": 30}
        if parsed.database in (None, "", ":memory:"):
            kwargs["poolclass"] = StaticPool
        else:
            Path(parsed.database).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url, **kwargs)
    if parsed.get_backend_name() == "sqlite":

        @event.listens_for(engine, "connect")
        def enable_foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    return engine
