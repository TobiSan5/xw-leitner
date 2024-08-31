import sys
from pathlib import Path

PROJ_DIR = Path(__file__).parent
PY_DIR = PROJ_DIR  # / "..."

if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from xw_leitner_core import *

