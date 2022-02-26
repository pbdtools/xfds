"""Default settings."""
import json
from pathlib import Path

INTERACTIVE = False
PROCESSORS = 1
CWD = Path.cwd()

DATA_DIR = Path(__file__).parent / "data"
SABALCORE_NODES_FILE = DATA_DIR / "sabalcore_nodes.json"
SABALCORE_NODES = json.loads(SABALCORE_NODES_FILE.read_text())
