import asyncio, aiohttp, random
URL = 'http://localhost:8000/v1/recommend'
async def do_call(session):
    uid = f'user_{random.randint(0,99)}'
    async with session.post(URL, json={'user_id': uid, 'k': 10}) as r:
        print(r.status, await r.text())
async def main():
    async with aiohttp.ClientSession() as s:
        tasks = [do_call(s) for _ in range(10)]
        await asyncio.gather(*tasks)
if __name__=='__main__':
    asyncio.run(main())
