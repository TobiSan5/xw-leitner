import sqlite3
import xlwings as xw

THIS_DIR = Path(__file__).parent
PROJ_DIR = THIS_DIR.parent
DB_FPATH = PROJ_DIR / "db/students.db"
DB_URL = f"sqlite:///{str(DB_FPATH)}"
XLSM_FPATH = PROJ_DIR / "xlsm/leitner_02.xlsm"

engine = sa.create_engine(DB_URL, echo=True)
SessionLocal = sa_orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare a base for your models
Base = sa_orm.declarative_base()


def get_db_session():
    """Create a new database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def main():
    raise NotImplementedError


def test():
    wb = xw.Book.caller()
    sh1 = wb.sheets[0]
    sh1_a1 = sh1["A1"]
    if sh1_a1.value == "You" or not sh1_a1.value:
        sh1_a1.value = "Hello"
    else:
        sh1_a1.value = "You"


if __name__ == "__main__":
    xw.Book(XLSM_FPATH).set_mock_caller()
    test()
