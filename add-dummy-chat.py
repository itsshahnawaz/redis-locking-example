from redis.asyncio.client import Redis
import asyncio
import sys

message = sys.argv[1]

STREAM_KEY = 'stream_key'

redis = Redis(
    host="redis",
    port="6379"
)

async def add_chat(msg):
    await redis.xadd(STREAM_KEY, {'msg': msg})

asyncio.run(add_chat(message))