from contextlib import contextmanager
import os
from pathlib import Path
from typing import Tuple

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
import xlwings as xw

THIS_DIR = Path(__file__).parent
PROJ_DIR = THIS_DIR.parent
DB_PATH = os.getenv("XW-LEITNER-DB-DIR")
XLSM_FPATH = PROJ_DIR / "xlsm/leitner_02.xlsm"

def get_db_url(db_filename: str) -> str:
    if not DB_PATH:
        raise EnvironmentError("Environment variable XW-LETINER-DB-DIR not set or empty.")
    return f"sqlite:///{str(Path(DB_PATH) / db_filename)}"

def get_engine(db_filename: str) -> Tuple[sa.engine.Engine, str]:
    db_url = get_db_url(db_filename)
    engine = sa.create_engine(db_url, echo=True)
    return (engine, db_url)


@contextmanager
def get_session(engine: sa.engine.Engine) -> sa_orm.Session:
    """Create a new database session."""
    SessionLocal = sa_orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def main():
    raise NotImplementedError


def test():
    pass


if __name__ == "__main__":
    xw.Book(XLSM_FPATH).set_mock_caller()
    test()
