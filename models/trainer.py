import json, numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

DATA_DIR = Path('data')
MODEL_DIR = Path('models')
MODEL_DIR.mkdir(exist_ok=True)
EMBED_DIM = 64

def load_apps(path=DATA_DIR/'sample_apps.json'):
    return json.loads(Path(path).read_text())

def build_item_embeddings(apps):
    docs = [ (a.get('title','') + ' ' + ' '.join(a.get('genres',[]))) for a in apps ]
    tfidf = TfidfVectorizer(max_features=2000)
    X = tfidf.fit_transform(docs)
    svd = TruncatedSVD(n_components=EMBED_DIM, random_state=42)
    E = svd.fit_transform(X)
    return E.astype('float32'), tfidf, svd

def export(embeddings, apps):
    np = __import__('numpy')
    np.save(MODEL_DIR/'item_embeddings.npy', embeddings)
    mapping = { apps[i]['app_id']: i for i in range(len(apps)) }
    (MODEL_DIR/'apps_index.json').write_text(json.dumps(mapping))
    print('Saved embeddings and mapping to models/')

if __name__=='__main__':
    apps = load_apps()
    E, tfidf, svd = build_item_embeddings(apps)
    export(E, apps)
