import asyncio, logging
from app.processing.consumer import ConsumerService
logging.basicConfig(level=logging.INFO)
svc = ConsumerService()
async def main():
    await svc.start()
    try:
        await svc.process_loop()
    finally:
        await svc.stop()
if __name__=='__main__':
    asyncio.run(main())
