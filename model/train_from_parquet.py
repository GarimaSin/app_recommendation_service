"""Train PyTorch model from a historical parquet dataset (produced by Feast or ETL).
If no parquet is available, falls back to synthetic data.
"""
import pandas as pd, os
import torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import mlflow
class ParquetDataset(Dataset):
    def __init__(self, path):
        self.df = pd.read_parquet(path)
        # Expect columns: user_id / item_id / label ; fallback mapping
        if 'user_id' not in self.df.columns:
            # map agent -> user_id and create item_id from metric hash as example
            self.df = self.df.rename(columns={'agent':'user_id'})
            self.df['item_id'] = self.df['metric'].astype('category').cat.codes
            self.df['label'] = (self.df['value']>0).astype(int)
    def __len__(self): return len(self.df)
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        return int(row['user_id']), int(row['item_id']), int(row['label'])
class RecModel(nn.Module):
    def __init__(self, n_user, n_item, dim=32):
        super().__init__()
        self.u = nn.Embedding(n_user, dim)
        self.v = nn.Embedding(n_item, dim)
        self.fc = nn.Sequential(nn.Linear(dim*2,64), nn.ReLU(), nn.Linear(64,1), nn.Sigmoid())
    def forward(self,u,i):
        return self.fc(torch.cat([self.u(u), self.v(i)], dim=-1)).squeeze(-1)
def train(parquet_path=None):
    mlflow.set_experiment('rec_pytorch_offline')
    with mlflow.start_run():
        if parquet_path and os.path.exists(parquet_path):
            ds = ParquetDataset(parquet_path)
            n_user = max(1000, ds.df['user_id'].max()+1)
            n_item = max(1000, ds.df['item_id'].max()+1)
            dl = DataLoader(ds, batch_size=256, shuffle=True)
            model = RecModel(n_user, n_item)
        else:
            print('Parquet not found - falling back to synthetic training')
            from model.train import SyntheticRecDataset, SimpleRecModel
            ds = SyntheticRecDataset(n=20000)
            dl = DataLoader(ds, batch_size=256, shuffle=True)
            model = SimpleRecModel(1000,1000)
        opt = optim.Adam(model.parameters(), lr=1e-3)
        crit = nn.BCELoss()
        for epoch in range(3):
            tot=0.0; cnt=0
            for batch in dl:
                u = torch.tensor(batch[0], dtype=torch.long)
                i = torch.tensor(batch[1], dtype=torch.long)
                l = torch.tensor(batch[2], dtype=torch.float)
                pred = model(u,i)
                loss = crit(pred,l)
                opt.zero_grad(); loss.backward(); opt.step()
                tot += loss.item(); cnt += 1
            print('Epoch', epoch, 'loss', tot/cnt)
        os.makedirs('model_artifacts', exist_ok=True)
        torch.save(model.state_dict(), 'model_artifacts/model_offline.pt')
        mlflow.pytorch.log_model(model, 'model_offline')
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--parquet', default='data/training_with_features.parquet')
    args = parser.parse_args()
    train(args.parquet)
