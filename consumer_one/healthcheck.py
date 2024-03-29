# # Sample code for stock_management.py
# print("Health Check microservice running...")
# # Add your stock management logic here
import pika
import pymongo
import json

# MongoDB connection parameters
MONGODB_HOST = "mongodb"
MONGODB_PORT = 27017
MONGODB_DATABASE = "inventory_db"

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = "health_check_queue"


def check_mongodb_connection():
    try:
        # Try to connect to MongoDB
        client = pymongo.MongoClient(
            host=MONGODB_HOST, port=MONGODB_PORT, serverSelectionTimeoutMS=2000
        )
        client.server_info()  # Test the connection
        return True, None
    except pymongo.errors.ServerSelectionTimeoutError as e:
        return False, str(e)


def check_rabbitmq_connection():
    try:
        # Try to connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        connection.close()
        return True, None
    except pika.exceptions.AMQPConnectionError as e:
        return False, str(e)


def perform_health_check():
    # Check MongoDB connection
    mongodb_status, mongodb_error = check_mongodb_connection()
    if mongodb_status:
        print("MongoDB connection: OK")
    else:
        print("MongoDB connection: Failed")
        print("Error:", mongodb_error)

    # Check RabbitMQ connection
    rabbitmq_status, rabbitmq_error = check_rabbitmq_connection()
    if rabbitmq_status:
        print("RabbitMQ connection: OK")
    else:
        print("RabbitMQ connection: Failed")
        print("Error:", rabbitmq_error)


def consume_message():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    # Define callback function to handle incoming messages
    def callback(ch, method, properties, body):
        message = json.loads(body.decode("utf-8"))
        print("Received message:", message)

        # Perform health check
        if "status" in message and message["status"] == "health_check":
            perform_health_check()

    # Consume messages from the queue
    channel.basic_consume(
        queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True
    )

    print("Waiting for health check messages...")
    channel.start_consuming()


if __name__ == "__main__":
    consume_message()


# import pika
# import time


# def main():
#     print("Healthcheck microservice running...")

#     try:
#         connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
#         channel = connection.channel()
#         channel.queue_declare(queue="item_queue")

#         def callback(ch, method, properties, body):
#             print("Received message:", body)

#         channel.basic_consume(
#             queue="item_queue", on_message_callback=callback, auto_ack=True
#         )

#         print("Waiting for messages...")
#         channel.start_consuming()

#     except Exception as e:
#         print("Error occurred:", e)


# if __name__ == "__main__":
#     main()
