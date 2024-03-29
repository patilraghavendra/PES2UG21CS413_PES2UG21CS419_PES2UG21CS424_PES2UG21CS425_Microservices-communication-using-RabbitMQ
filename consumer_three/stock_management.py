import pika
import json
from pymongo import MongoClient

# MongoDB connection parameters
MONGODB_HOST = "host.docker.internal"
MONGODB_PORT = 27017
MONGODB_DATABASE = "inventory_db"
MONGODB_COLLECTION = "inventory"

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_UPDATE_QUEUE = "item_queue"


def update_document_in_mongodb(product_id, updated_data):
    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]

        # Update the document in MongoDB
        db[MONGODB_COLLECTION].update_one(
            {"product_id": product_id}, {"$set": updated_data}
        )

        print(f"Document updated for product ID {product_id}")

    except Exception as e:
        print("Error updating document in MongoDB:", str(e))


def consume_update_messages():
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=RABBITMQ_UPDATE_QUEUE)

        # Define callback function to handle incoming messages
        def callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            print("Received message:", message)

            # Check if the message contains product_id and updated_data
            if "product_id" in message and "updated_data" in message:
                # Update the document in MongoDB
                update_document_in_mongodb(
                    message["product_id"], message["updated_data"]
                )

        # Consume messages from the queue
        channel.basic_consume(
            queue=RABBITMQ_UPDATE_QUEUE, on_message_callback=callback, auto_ack=True
        )

        print("Waiting for update messages...")
        channel.start_consuming()

    except Exception as e:
        print("Error consuming update messages:", str(e))


if __name__ == "__main__":
    consume_update_messages()
