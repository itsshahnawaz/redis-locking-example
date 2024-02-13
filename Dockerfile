# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./main.py /app/main.py
COPY ./test.py /app/test.py

# Install additional dependencies
RUN pip install python-socketio[asyncio_client] python-socketio[asyncio_server] fastapi_cache2[redis] requests websocket-client

# Expose port
EXPOSE 8000