from flask import Flask, jsonify, request
import pika
import json

app = Flask(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_ITEM_QUEUE = "item_queue"
RABBITMQ_HEALTHCHECK_QUEUE = "healthcheck_queue"
RABBITMQ_ORDER_QUEUE = "order_queue"


def send_health_check_message():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_HEALTHCHECK_QUEUE)

    # Prepare the health check message
    message = {"status": "health_check"}

    # Publish the message to the queue
    channel.basic_publish(
        exchange="", routing_key=RABBITMQ_HEALTHCHECK_QUEUE, body=json.dumps(message)
    )

    print("Health check message sent to RabbitMQ")

    # Close the connection
    connection.close()


def send_create_request(data):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_ITEM_QUEUE)

    # Prepare the create request message
    message = {"action": "create_item", "data": data}

    # Publish the message to the queue
    channel.basic_publish(
        exchange="", routing_key=RABBITMQ_ITEM_QUEUE, body=json.dumps(message)
    )

    print("Create request sent to RabbitMQ")

    # Close the connection
    connection.close()


def send_update_request(product_id, updated_data):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_ITEM_QUEUE)

    # Prepare the update request message
    message = {"product_id": product_id, "updated_data": updated_data}

    # Publish the message to the queue
    channel.basic_publish(
        exchange="", routing_key=RABBITMQ_ITEM_QUEUE, body=json.dumps(message)
    )

    print("Update request sent to RabbitMQ")

    # Close the connection
    connection.close()


def send_read_request():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_ITEM_QUEUE)

    # Prepare the read request message for all items
    message = {"action": "read_all_items"}

    # Publish the message to the queue
    channel.basic_publish(
        exchange="", routing_key=RABBITMQ_ITEM_QUEUE, body=json.dumps(message)
    )

    print("Read all items request sent to RabbitMQ")

    # Close the connection
    connection.close()


def send_delete_request(item_id):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_ITEM_QUEUE)

    # Prepare the delete request message
    message = {"action": "delete_item", "item_id": item_id}

    # Publish the message to the queue
    channel.basic_publish(
        exchange="", routing_key=RABBITMQ_ITEM_QUEUE, body=json.dumps(message)
    )

    print("Delete request sent to RabbitMQ")

    # Close the connection
    connection.close()


@app.route("/health_check", methods=["GET"])
def health_check():
    send_health_check_message()
    return jsonify({"message": "Health check message sent"}), 200


@app.route("/create_item", methods=["POST"])
def create_item():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    send_create_request(data)
    return jsonify({"message": "Create request sent"}), 200


@app.route("/update_item/<product_id>", methods=["PUT"])
def update_item(product_id):
    updated_data = request.json
    if not updated_data:
        return jsonify({"error": "No data provided"}), 400
    send_update_request(product_id, updated_data)
    return jsonify({"message": "Update request sent"}), 200


@app.route("/read_items", methods=["GET"])
def read_items():
    send_read_request()
    return jsonify({"message": "Read all items request sent"}), 200


@app.route("/delete_item/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    send_delete_request(item_id)
    return jsonify({"message": f"Delete request sent for item with ID {item_id}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
