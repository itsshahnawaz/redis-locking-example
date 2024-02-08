from fastapi import FastAPI
import socketio
import asyncio
from redis.asyncio.client import Redis
from redis.asyncio.lock import Lock
from uvicorn import run

app = FastAPI()

redis = Redis(
    host="redis",
    port="6379"
)

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi",)
app.mount("", socketio.ASGIApp(sio))

REDIS_TEST_KEY = "key"

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")
    
    # Create a new lock that will timeout in 2 seconds
    lock = Lock(redis, "update_lock", timeout=2)

    lock_acquired = False

    # Keep trying to acquire the lock
    while not lock_acquired:
        acquired = await lock.acquire(blocking=False, blocking_timeout=20)
        # If lock is acquired, update the key
        if acquired:
            lock_acquired = await redis.set(REDIS_TEST_KEY, "pre-connect")
        else:
            print(f"Failed to acquire lock; client {sid}, retrying...")
        # Introduce 100ms wait to avoid too many acquisition requests
        await asyncio.sleep(0.1)
    await redis.set(REDIS_TEST_KEY, 'post-connect')

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    # Create a new lock that will timeout in 6 seconds(As our disconnect takes more time)
    lock = Lock(redis, "update_lock", timeout=6)

    lock_acquired = False

    acquired = await lock.acquire(blocking=True, blocking_timeout=10)
    if acquired:
        lock_acquired = await redis.set(REDIS_TEST_KEY, "pre-disconnect")
    
    if lock_acquired:
        # Fake api call behavior
        await asyncio.sleep(4)
        await redis.set(REDIS_TEST_KEY, "post-disconnect")
        await asyncio.sleep(4)

if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, workers=4)
