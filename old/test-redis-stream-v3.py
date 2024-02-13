import requests
import asyncio
from random import randint

async def main():
    ID = randint(0, 100)
    response = requests.post(f"http://127.0.0.1:8000/stream/{ID}")
    print(response.text)
    response = requests.get(f"http://127.0.0.1:8000/stream/{ID}", stream=True)
    for chunk in response.iter_content(chunk_size=None):
        if chunk:
            print(chunk.decode(), end='', flush=True)

asyncio.run(main())