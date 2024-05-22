from kombu import Connection, Exchange, Queue
import json

def send_telemetry_data(data):
    with Connection('amqp://user:password@localhost:5672/') as connection:
        exchange = Exchange('poc_exchange', type='direct')
        queue = Queue('poc_queue', exchange=exchange, routing_key='poc_routing')

        with connection.Producer() as producer:
            producer.publish(
                body=data,
                exchange=exchange,
                routing_key='poc_routing',
                serializer='json',
                declare=[queue],
                priority=5
            )

message = {
    "id": "158195-asfasf-135059",
    "content": "Lorem Ipsum",
}

message_json = json.dumps(message)

# Single Test
# send_telemetry_data(message_json)

# Stress Test
for _ in range(1400):
    send_telemetry_data(message_json)