import json
from pathlib import Path
def load_catalog(path=Path('data')/'sample_apps.json'):
    return json.loads(path.read_text())
