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

def fake_ai(message):
    if message == 'Hi':
        return "Hi! How are you?"
    else:
        return "How can I help?"

async def stream_text(response_message):
    for itr in range(len(response_message)):
        await asyncio.sleep(0.05)
        yield str.encode(response_message[itr])

@app.get("/stream")
async def main():
    message = 'Hi'
    written = await add_to_redis_stream(message)
    response_message = fake_ai(message=message)
    await add_to_redis_stream(response_message)
    message_text = await read_from_redis_stream(written)
    decoded_msg = message_text.decode()
    return StreamingResponse(stream_text(decoded_msg))

# =============================NEW=================================
async def read_from_redis_stream(message_id):
    try:
        start_id = message_id
        message_data = await redis.xread({'stream_key': start_id}, block=0, count=1)
        message_id = message_data[0][1][0][0]
        message_text = message_data[0][1][0][1]
        return message_text[b'msg']
    except Exception as e:
        print('==========e: ', e)

async def add_to_redis_stream(message):
    return await redis.xadd(STREAM_KEY, {'msg': message})