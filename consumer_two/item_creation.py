# # item_creation.py

# from pymongo import MongoClient
# import pika
# import json

# # MongoDB connection parameters
# MONGODB_HOST = "host.docker.internal"
# MONGODB_PORT = 27017
# MONGODB_DATABASE = "inventory_db"
# MONGODB_COLLECTION = "inventory"

# # RabbitMQ connection parameters
# RABBITMQ_HOST = "rabbitmq"
# RABBITMQ_PORT = 5672
# RABBITMQ_QUEUE = "item_queue"


# def insert_into_database(message):
#     # Connect to MongoDB
#     client = MongoClient(MONGODB_HOST, MONGODB_PORT)

#     # Access the database
#     db = client[MONGODB_DATABASE]

#     # Access the collection
#     collection = db[MONGODB_COLLECTION]

#     # Insert the message into the collection
#     collection.insert_one(message)
#     print("Inserted message into MongoDB:", message)


# def consume_message():
#     # Connect to RabbitMQ
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
#     )
#     channel = connection.channel()

#     # Declare the queue
#     channel.queue_declare(queue=RABBITMQ_QUEUE)

#     # Define callback function to handle incoming messages
#     def callback(ch, method, properties, body):
#         message = json.loads(body.decode("utf-8"))
#         print("Received message:", message)

#         # Insert the message into the database
#         insert_into_database(message)

#     # Consume messages from the queue
#     channel.basic_consume(
#         queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True
#     )

#     print("Waiting for messages...")
#     channel.start_consuming()


# if __name__ == "__main__":
#     consume_message()

# Sample code for item_creation.py
print("Item creation microservice running...")
# Add your item creation logic here
