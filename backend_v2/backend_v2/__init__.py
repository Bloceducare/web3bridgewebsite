import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# This allows easy placement of apps within the interior
# apps directory.
sys.path.append(str(BASE_DIR / "apps"))