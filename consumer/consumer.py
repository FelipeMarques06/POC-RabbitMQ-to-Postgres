from kombu import Connection, Exchange, Queue, Consumer
import json
import psycopg2
import os
import time
import logging

logging.basicConfig(level=logging.INFO)

def process_and_store_data(data):
    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host='postgres'
    )
    cur = conn.cursor()
    
    cur.execute("INSERT INTO my_table (data) VALUES (%s)", (json.dumps(data),))
    
    conn.commit()
    cur.close()
    conn.close()

def handle_message(body, message):
    try:
        data = json.loads(body)
        logging.info(f"Received message: {data}")
        process_and_store_data(data)
        message.ack()
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON data: {e}")
        message.reject()
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        message.reject()
        import traceback
        logging.error(traceback.format_exc())

def start_consumer():
    amqp_url = 'amqp://user:password@rabbitmq:5672/'
    exchange_name = 'poc_exchange'
    queue_name = 'poc_queue'

    while True:
        try:
            with Connection(amqp_url) as conn:
                exchange = Exchange(exchange_name, type='direct', durable=True)
                queue = Queue(name=queue_name, exchange=exchange, routing_key='poc_routing', durable=True)

                with Consumer(conn, queues=queue, callbacks=[handle_message], prefetch_count=1):
                    logging.info('Consumer ready. Waiting for messages...')
                    while True:
                        conn.drain_events()

        except Exception as e:
            logging.error(f'Connection failed: {e}')
            logging.info('Retrying in 5 seconds...')
            time.sleep(5)

if __name__ == '__main__':
    start_consumer()

