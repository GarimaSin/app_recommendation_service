#!/usr/bin/env python3
"""Extract historical events from ClickHouse and write to Parquet files for training.
Usage: python etl/extract_clickhouse.py --start '2025-01-01' --end '2025-01-31' --out data/training.parquet
"""
import argparse, os
from clickhouse_connect import get_client
import pandas as pd
def extract(start, end, out):
    client = get_client(host=os.getenv('CLICKHOUSE_HOST','clickhouse'), port=8123, database=os.getenv('CLICKHOUSE_DB','default'))
    q = f"""SELECT ts, agent, metric, value, tags FROM events WHERE ts >= toDateTime('{start}') AND ts < toDateTime('{end}')"""
    print('Running query:', q)
    df = client.query_df(q)
    print('Rows extracted:', len(df))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_parquet(out, index=False)
    print('Wrote parquet to', out)
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', required=True)
    parser.add_argument('--end', required=True)
    parser.add_argument('--out', default='data/training.parquet')
    args = parser.parse_args()
    extract(args.start, args.end, args.out)
