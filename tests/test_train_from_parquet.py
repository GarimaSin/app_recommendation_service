import pandas as pd, torch, os, tempfile
from model.train_from_parquet import train, ParquetDataset
def test_train_from_parquet(tmp_path):
    df = pd.DataFrame([{'ts':'2025-01-01 00:00:00','agent':0,'metric':'x','value':1.0}])
    inp = tmp_path / 'train.parquet'
    df.to_parquet(str(inp), index=False)
    # run train which should create model_artifacts/model_offline.pt
    train(str(inp))
    assert os.path.exists('model_artifacts/model_offline.pt')
