from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import socketio
from redis.asyncio.client import Redis
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import asyncio
import json

app = FastAPI()

redis = Redis(host="redis", port="6379")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode="asgi",
)
app.mount("/socket-app", socketio.ASGIApp(sio))


@sio.event
async def response(sid, data):
    await redis.xadd(data["chat_id"], {"data": json.dumps(data)})


def decode_dict(byte_encoded):
    converted_dict = {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in byte_encoded.items()
    }
    return converted_dict


async def stream_chat_data(chat_id):
    start_id = 0
    while True:
        message_data = await redis.xread({chat_id: start_id}, count=1)
        if message_data:
            start_id = message_data[0][1][0][0]
            data = decode_dict(message_data[0][1][0][1])
            data_dict = json.loads(data["data"])
            message = data_dict["message"]
            if message == "STOP":
                await redis.delete(chat_id)
                break
            yield message


@app.post("/chat_stream")
async def main(request: Request):
    body = await request.json()
    await sio.emit(
        "message", {"message": body.get("message"), "chat_id": body.get("chat_id")}
    )
    return StreamingResponse(stream_chat_data(body.get("chat_id")))
