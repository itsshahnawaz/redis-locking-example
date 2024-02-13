from socketio import AsyncClient
import asyncio

sio = AsyncClient(
    reconnection_attempts=0,
    reconnection_delay=1,
)


async def get_ai_response(message):
    await asyncio.sleep(3)
    for word in ["Hi", ", ", "there ", "\n", "How ", "are ", "you", "?"]:
        await asyncio.sleep(1)
        yield word


@sio.event
async def connect():
    print("connection established")


@sio.event
async def message(data):
    print("message received with ", data)
    async for item in get_ai_response(data["message"]):
        await sio.emit("response", {"message": item, "chat_id": data["chat_id"]})
    await sio.emit("response", {"message": "STOP", "chat_id": data["chat_id"]})


@sio.event
async def disconnect():
    print("disconnected from server")


async def main():
    await connect()
    await sio.wait()


async def connect():
    await sio.connect(
        "http://localhost:8000",
        wait_timeout=5,
        socketio_path="/socket-app/socket.io",
    )


asyncio.run(main())
