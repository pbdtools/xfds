"""Default settings."""
from pathlib import Path

INTERACTIVE = False
PROCESSORS = 1
CWD = Path.cwd()

DATA_DIR = Path(__file__).parent / "data"
SABALCORE_NODES = DATA_DIR / "sabalcore_nodes.json"
