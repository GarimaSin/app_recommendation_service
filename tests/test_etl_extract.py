import os, pandas as pd, pyarrow as pa, pyarrow.parquet as pq, tempfile
from etl.extract_clickhouse import extract
def test_extract_parquet(tmp_path, monkeypatch):
    # monkeypatch clickhouse client to return a dataframe
    class DummyClient:
        def __init__(self, *args, **kwargs): pass
        def query_df(self, q):
            return pd.DataFrame([{'ts':'2025-01-01 00:00:00','agent':'a','metric':'cpu','value':1.0,'tags':'{}'}])
    monkeypatch.setenv('CLICKHOUSE_HOST','localhost')
    monkeypatch.setattr('clickhouse_connect.get_client', lambda host, port, database: DummyClient())
    out = tmp_path / 'out.parquet'
    extract('2025-01-01','2025-01-02', str(out))
    assert out.exists()
    df = pd.read_parquet(str(out))
    assert len(df) == 1
