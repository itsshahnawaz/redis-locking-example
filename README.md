This repo contains code to replicate race condition along with the solution.
It's a dockerized app and following are the commands to run it:

Running for the first time:
docker-compose up --build

Later:
docker-compose up --build

SSH into container:
docker exec -it flask-testing-app_app_1 /bin/bash

**Testing flow**
Prerequisites:
> Install redis inside container
> RUN: apt-get update
> RUN: apt-get install redis-tools

After:
> RUN: python test.py
> This will create a key in redis and keep a lock on it
> Press ctrl+c to kill the process, which will disconnect the socket.
> Socket disconnect event will trigger and then again run the app with "python test.py"
> The disconnect will create a lock and hold it until it completes.
> After that, the connect will write on the key.
