"""Create point-in-time-correct training dataset using Feast.
This script shows a typical pattern: you must have a Feast repo initialized (feast/).
It will load the entity rows from the extracted ClickHouse parquet and request historical features.
"""
import pandas as pd, os, argparse
from feast import FeatureStore
def create(training_parquet, output_parquet):
    print('Loading extracted events from', training_parquet)
    df = pd.read_parquet(training_parquet)
    # For demonstration, assume entity is 'agent' and event timestamp column is 'ts'
    # Build entity_rows for Feast: a list of dicts with entity id and event_timestamp
    entity_rows = df[['agent','ts']].drop_duplicates().rename(columns={'agent':'user_id','ts':'event_timestamp'})
    # Format event_timestamp to pandas datetime if not already
    entity_rows['event_timestamp'] = pd.to_datetime(entity_rows['event_timestamp'])
    # write entity rows to a temporary csv for demo
    entity_rows_path = 'data/entity_rows.csv'
    entity_rows.to_csv(entity_rows_path, index=False)
    print('Entity rows written to', entity_rows_path)
    # Initialize Feast FeatureStore (expects feast/feature_store.yaml)
    store = FeatureStore(repo_path='feast')
    # Example: request historical features; feature_refs must match feast definitions in feast/core.py
    feature_refs = []  # e.g., ['user_features:click_count', 'item_features:ctr']
    if len(feature_refs)==0:
        print('No feature_refs defined in this demo script. Edit create_historical_dataset to include your feature refs.')
        # fallback: just copy original df to output
        df.to_parquet(output_parquet, index=False)
        print('Wrote output dataset to', output_parquet)
        return
    # In real deployment, you would call store.get_historical_features as shown below:
    # entity_df = pd.read_csv(entity_rows_path)
    # training_df = store.get_historical_features(entity_rows=entity_df, feature_refs=feature_refs).to_df()
    # training_df.to_parquet(output_parquet, index=False)
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='inp', required=True)
    parser.add_argument('--out', dest='out', default='data/training_with_features.parquet')
    args = parser.parse_args()
    create(args.inp, args.out)
