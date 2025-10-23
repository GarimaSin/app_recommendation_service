import pandas as pd, tempfile, os
from feast.create_historical_dataset import create
def test_create_historical_dataset(tmp_path, monkeypatch):
    # create a small parquet file
    df = pd.DataFrame([{'ts':'2025-01-01 00:00:00','agent':'1','metric':'cpu','value':1.0,'tags':'{}'}])
    inp = tmp_path / 'in.parquet'
    out = tmp_path / 'out.parquet'
    df.to_parquet(str(inp), index=False)
    # monkeypatch feast.FeatureStore to avoid making calls
    class DummyFS:
        def __init__(self, repo_path=None): pass
    monkeypatch.setattr('feast.FeatureStore', DummyFS)
    # call create with no feature refs (function will fallback to copy)
    create(str(inp), str(out))
    assert out.exists()
