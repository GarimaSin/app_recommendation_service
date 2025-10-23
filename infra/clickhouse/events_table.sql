CREATE TABLE IF NOT EXISTS events (
    ts DateTime,
    agent String,
    metric String,
    value Float64,
    tags String
) ENGINE = MergeTree() ORDER BY ts;
