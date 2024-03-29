import pika
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection parameters
MONGODB_HOST = "host.docker.internal"
MONGODB_PORT = 27017
MONGODB_DATABASE = "inventory_db"

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672

def check_mongodb_connection():
    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[MONGODB_DATABASE]

        # Check if the connection is successful by listing collections
        collections = db.list_collection_names()
        return True, f"MongoDB Connection Successful. Collections: {collections}"
    except Exception as e:
        return False, f"MongoDB Connection Failed. Error: {str(e)}"

def check_rabbitmq_connection():
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        connection.close()
        return True, "RabbitMQ Connection Successful"
    except Exception as e:
        return False, f"RabbitMQ Connection Failed. Error: {str(e)}"

def perform_health_check():
    # Check MongoDB connection
    mongodb_status, mongodb_message = check_mongodb_connection()
    print(f"{datetime.now()} - MongoDB Health Check: {'Success' if mongodb_status else 'Failure'}. {mongodb_message}")

    # Check RabbitMQ connection
    rabbitmq_status, rabbitmq_message = check_rabbitmq_connection()
    print(f"{datetime.now()} - RabbitMQ Health Check: {'Success' if rabbitmq_status else 'Failure'}. {rabbitmq_message}")

if __name__ == "__main__":
    perform_health_check()
