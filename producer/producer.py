# producer.py

import pika
import json
import time

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = "item_queue"


def send_health_check_message():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    # Prepare the health check message
    message = {"status": "health_check"}

    # Publish the message to the queue
    channel.basic_publish(
        exchange="", routing_key=RABBITMQ_QUEUE, body=json.dumps(message)
    )

    print("Health check message sent to RabbitMQ")

    # Close the connection
    connection.close()


# def publish_message(message):
#     # Connect to RabbitMQ
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
#     )
#     channel = connection.channel()

#     # Declare the queue
#     channel.queue_declare(queue=RABBITMQ_QUEUE)

#     # Convert message to JSON
#     json_message = json.dumps(message)

#     # Publish the message to the queue
#     channel.basic_publish(exchange="", routing_key=RABBITMQ_QUEUE, body=json_message)

#     print("Message sent to", RABBITMQ_QUEUE, ":", message)

#     # Close the connection
#     connection.close()


if __name__ == "__main__":
    # Example message to publish
    # message = {"id": 1, "name": "Example Item", "quantity": 10}
    while True:
        send_health_check_message()
        # Sleep for 60 seconds before sending the next health check message
        time.sleep(60)
    # publish_message(message)
