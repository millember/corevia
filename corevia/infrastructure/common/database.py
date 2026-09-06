import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from corevia.infrastructure.common.orm import models  # noqa: F401
from corevia.infrastructure.common.orm.base import Base

DEFAULT_DATA_DIR = Path.home() / ".local" / "share" / "corevia"

APP_DATA_DIR = Path(os.environ.get("COREVIA_DATA_DIR", DEFAULT_DATA_DIR))

APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = APP_DATA_DIR / "corevia.db"

engine = create_engine(f"sqlite:///{DATABASE_PATH}", future=True)


@event.listens_for(Engine, "connect")
def configure_sqlite(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()


SessionFactory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Database:
    @staticmethod
    def initialize() -> None:
        Base.metadata.create_all(engine)
