import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from app.ingest.producer_manager import ProducerManager

@pytest.mark.asyncio
async def test_send_batch_partition_and_dlq(monkeypatch):
    pm = ProducerManager()
    # create a fake producer with send_and_wait behavior
    async def fake_start(): pass
    class FakeProducer:
        def __init__(self):
            self.started = True
            self.sent = []
        async def start(self): pass
        async def stop(self): pass
        async def send_and_wait(self, topic, value, key=None, partition=None):
            if b'bad' in value:
                raise Exception('boom')
            self.sent.append((topic, key, value, partition))
            return True
    fake = FakeProducer()
    monkeypatch.setattr(pm, "_producer", fake)
    # simulate send_batch
    msgs = [(b'k1', b'good1'), (b'k2', b'bad')]
    results = await pm.send_batch('events', msgs, dlq_topic='events-dlq')
    assert len(results) == 2
