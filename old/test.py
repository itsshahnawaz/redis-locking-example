from socketio import AsyncClient
import asyncio

sio = AsyncClient(
    reconnection_attempts=0,
    reconnection_delay=1,
)

async def connect():
    await sio.connect('http://localhost:8000', wait_timeout=10)

async def main():
    await connect()
    await sio.wait()


asyncio.run(main())