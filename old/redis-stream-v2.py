from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from redis.asyncio.client import Redis
import asyncio
from fastapi.middleware.cors import CORSMiddleware

STREAM_KEY = 'stream_key'

redis = Redis(
    host="redis",
    port="6379"
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def fake_chat_app():
    return read_from_redis_stream()


@app.get("/stream")
async def main():
    return StreamingResponse(await fake_chat_app())

# =============================NEW=================================
async def read_from_redis_stream():
    start_id = 0
    while True:
        message_data = await redis.xread({STREAM_KEY: start_id}, block=5000, count=1)
        if len(message_data) == 0:
            break
        message_id = message_data[0][1][0][0]
        message_text = message_data[0][1][0][1]
        start_id = message_id
        yield message_text[b'msg']