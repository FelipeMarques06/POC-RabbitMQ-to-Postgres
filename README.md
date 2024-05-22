# What's this?
This is a POC I made for work to test RabbitMQ and transform/consume data to Postgres.
There are probably a thousand better ways of doing this, if you know one, please let me know.
<br/>
I've uploaded this code here in case I need it anytime in the future.
Also, I didn't take Postgres too much into consideration as I did this to learn how to publish and consume data using RabbitMQ.

# Instructions

## You need to have

- Docker
- Python

## Create a venv, active it and install dependencies
- python -m venv venv
- LINUX: source venv/bin/activate
- WINDOWS: source venv/Scripts/activate
- pip install -r requirements/base.txt

## Run docker-compose

docker-compose -f docker-compose/dev.yml up -d --build

## Run Postgres scripts

Create table:
- docker exec -it postgres psql -U postgres -d mydatabase -c "CREATE TABLE my_table (id SERIAL PRIMARY KEY, data JSONB);"

Create role root:
- docker exec -it postgres psql -U postgres -d mydatabase -c "CREATE ROLE root LOGIN;"

## Run the request inside /requests

The file is called kombupub.py. It's a simple publish code.
You're free to change exchange, queue and routing_key names (if you do so, you also need to change in consumer.py).
But check consumer logs before for the message: "Consumer ready. Waiting for messages..."

## Useful commands

Access database to query data:
- docker exec -it postgres psql -U postgres -d mydatabase

## Improving the example

- Incorporate Postgres scripts to docker-compose or something else.
- Code clean up.

## Technologies used

- Docker
- Python
- RabbitMQ
- Postgres
