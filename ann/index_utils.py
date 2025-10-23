from annoy import AnnoyIndex
from pathlib import Path
import numpy as np

def load_index(dim=64):
    idx = AnnoyIndex(dim, metric='angular')
    idx.load(str(Path('models')/'items.ann'))
    emb = np.load(Path('models')/'item_embeddings.npy')
    return idx, emb
