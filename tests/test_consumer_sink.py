import pytest
from unittest.mock import MagicMock, patch
from app.processing.consumer import ClickHouseSink
def test_bulk_insert_calls_client():
    mock_client = MagicMock()
    sink = ClickHouseSink()
    sink.client = mock_client
    rows = [{'ts': '2025-01-01 00:00:00', 'agent':'a', 'metric':'cpu', 'value':1.0, 'tags':'{}'}]
    sink.bulk_insert('events', rows)
    assert mock_client.insert.called
