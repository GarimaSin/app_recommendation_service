from annoy import AnnoyIndex
import numpy as np
from pathlib import Path
def build_annoy(dim=64, n_trees=50):
    emb = np.load(Path('models')/'item_embeddings.npy')
    idx = AnnoyIndex(dim, metric='angular')
    for i,v in enumerate(emb):
        idx.add_item(i, v.tolist())
    idx.build(n_trees)
    idx.save(str(Path('models')/'items.ann'))
    print('Saved Annoy index to models/items.ann')

if __name__=='__main__':
    build_annoy()
