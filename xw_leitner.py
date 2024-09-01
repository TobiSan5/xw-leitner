import os
import sys
from pathlib import Path

import xlwings as xw

PROJ_DIR = Path(__file__).parent
PY_DIR = PROJ_DIR  # / "..."

if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from xw_leitner_core import *  # (imports xw, etc.)

def test():
    wb = xw.Book.caller()

    dialogue_rng = wb.names["dialogue_rng"].refers_to_range
    db_fname_rng = wb.names["db_fname"].refers_to_range
    db_path_rng = wb.names["db_path"].refers_to_range

    engine, db_url = get_engine(db_fname_rng.value)

    db_path_rng.value = db_url

    with get_session(engine) as session:
        dialogue_rng.value = ", ".join([obj.group_name for obj in session.query(Group).all()])


if __name__ == "__main__":
    try:
        caller_fpath = Path().cwd() / sys.argv[1]
    except:
        raise SyntaxError("Give filepath to workbook as first argument!")
    wb = xw.Book(caller_fpath).set_mock_caller()
    test()