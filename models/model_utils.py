import numpy as np
from pathlib import Path

def load_item_embeddings(path=Path('models')/'item_embeddings.npy'):
    return np.load(path)

def load_apps_index(path=Path('models')/'apps_index.json'):
    import json
    return json.loads(Path(path).read_text())
