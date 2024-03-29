# print("Performing order_processing")
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
RABBITMQ_ORDER_QUEUE = "item_queue"


def read_all_documents_from_mongodb():
    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]

        # Retrieve all documents from MongoDB
        documents = db[MONGODB_COLLECTION].find()

        return documents
    except Exception as e:
        print("Error reading documents from MongoDB:", str(e))
        return None


def process_order_message(order_message):
    try:
        # Extract order_id from the message
        order_id = order_message.get("order_id")

        # Read all documents from MongoDB
        documents = read_all_documents_from_mongodb()

        if documents:
            # Print all documents
            print("All documents in MongoDB:")
            for document in documents:
                print(document)
        else:
            print("No documents found in MongoDB")

    except Exception as e:
        print("Error processing order message:", str(e))


def consume_read_messages():
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=RABBITMQ_ORDER_QUEUE)

        # Define callback function to handle incoming messages
        def callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            print("Received message:", message)

            # Process the received message
            process_order_message(message)

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Consume messages from the queue
        channel.basic_consume(queue=RABBITMQ_ORDER_QUEUE, on_message_callback=callback)

        print("Waiting for read messages...")
        channel.start_consuming()

    except Exception as e:
        print("Error consuming read messages:", str(e))


if __name__ == "__main__":
    consume_read_messages()
