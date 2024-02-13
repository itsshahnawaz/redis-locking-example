import requests
import asyncio


async def main():
    response = requests.post(
        "http://127.0.0.1:8000/chat_stream/",
        json={"message": "Hi", "chat_id": "123"},
        stream=True,
    )
    for chunk in response.iter_content(chunk_size=1):
        if chunk:
            print(chunk.decode(), end="", flush=True)


asyncio.run(main())
