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
RABBITMQ_ITEM_QUEUE = "item_queue"


def delete_from_mongodb(item_id):
    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]

        # Delete document from MongoDB collection
        result = db[MONGODB_COLLECTION].delete_one({"product_id": item_id})

        if result.deleted_count > 0:
            print(f"Document deleted from MongoDB for product ID {item_id}")
        else:
            print(f"No document found in MongoDB for product ID {item_id}")
    except Exception as e:
        print("Failed to delete document from MongoDB:", str(e))


def consume_messages():
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=RABBITMQ_ITEM_QUEUE)

        # Define callback function to handle incoming messages
        def callback(ch, method, properties, body):
            message = json.loads(body.decode("utf-8"))
            print("Received delete message:", message)

            # Check if the message is for item deletion
            if "action" in message and message["action"] == "delete_item":
                # Extract item ID and delete from MongoDB
                item_id = message.get("item_id")
                if item_id:
                    delete_from_mongodb(item_id)
                else:
                    print("No item ID provided in delete message")

        # Consume messages from the queue
        channel.basic_consume(
            queue=RABBITMQ_ITEM_QUEUE, on_message_callback=callback, auto_ack=True
        )

        print("Waiting for delete messages...")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"RabbitMQ connection error: {e}")
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    consume_messages()
