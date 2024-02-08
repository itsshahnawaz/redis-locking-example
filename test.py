from socketio import AsyncClient
import asyncio

sio = AsyncClient(
    reconnection_attempts=0,
    reconnection_delay=1,
)

async def connect():
    print("====START CONNECT====")
    await sio.connect('http://localhost:8000', wait_timeout=10)

async def main():
    try:
        print("====MAIN====")
        await connect()
        print("====CONNECTED====")
        await sio.wait()
    except Exception as e:
        print('====Exception: ', e)


asyncio.run(main())