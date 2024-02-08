# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./main.py /app/main.py
COPY ./test.py /app/test.py

# Install additional dependencies
RUN pip install python-socketio[asyncio_client] python-socketio[asyncio_server] fastapi_cache2[redis] requests websocket-client

# Expose port
EXPOSE 8000

# Command to run the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", '--workers', '4']
# CMD ["python", "main.py"]
# uvicorn main:app --host "0.0.0.0" --port 8000