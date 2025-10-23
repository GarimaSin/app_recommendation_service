import numpy as np
import json
from pathlib import Path
from annoy import AnnoyIndex

MODEL_DIR = Path('models')
DIM = 64

class Recommender:
    def __init__(self):
        self.dim = DIM
        self.index = AnnoyIndex(self.dim, metric='angular')
        self.index.load(str(MODEL_DIR/'items.ann'))
        self.apps_index = json.loads((MODEL_DIR/'apps_index.json').read_text())
        self.index_to_app = {int(v): k for k,v in self.apps_index.items()}
        self.emb = np.load(MODEL_DIR/'item_embeddings.npy')

    def recommend_by_vector(self, vec: np.ndarray, k=10):
        v = np.array(vec, dtype=np.float32)
        v = v / (np.linalg.norm(v) + 1e-9)
        ids, dists = self.index.get_nns_by_vector(v.tolist(), n=k, include_distances=True)
        return [ self.index_to_app.get(i) for i in ids if i in self.index_to_app ]

    def recommend_popular(self, k=10):
        # simple popularity fallback using apps_index ordering
        return list(self.apps_index.keys())[:k]

    def get_default_vector(self):
        # return mean item vector as cold-start
        return np.mean(self.emb, axis=0)
