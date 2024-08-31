import sys
from pathlib import Path

THIS_DIR = Path(__file__).parent
PROJ_DIR = THIS_DIR.parent
PY_DIR = PROJ_DIR / "py"

if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from xl_interface import main

