from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from redis.asyncio.client import Redis
import asyncio
from fastapi.middleware.cors import CORSMiddleware

STREAM_KEY = 'stream_key'

redis = Redis(
    host="localhost",
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
async def add_response(id):
    await asyncio.sleep(3)
    for t in ["Hi", ", ", "there ", "\n", "How ", "are ", "you", "?"]:
        await redis.xadd(id, {"msg":t})
        await asyncio.sleep(2)
    await redis.xadd(id, {"msg":"Stop", "stop": "finish"})

async def fake_chat_app(id:str):
    async for m in read_from_redis_stream(id=id):
        yield m


@app.post("/stream/{id}")
async def main(id:str, background_task:BackgroundTasks):
    background_task.add_task(add_response, id)
    return b"stream is started"

@app.get("/stream/{id}")
async def main(id:str):
    return StreamingResponse(fake_chat_app(id))

# =============================NEW=================================
async def read_from_redis_stream(id:str):
    print('============id: ', id)
    start_id = 0
    while True:
        message_data = await redis.xread({id: start_id}, count=1)
        print('========message_data: ', message_data)
        if message_data:
            start_id = message_data[0][1][0][0]
            message_text = message_data[0][1][0][1]
            if message_text.get(b"stop"):

                await redis.delete(id)
                break
            yield message_text[b'msg']
        else:
            await asyncio.sleep(1)