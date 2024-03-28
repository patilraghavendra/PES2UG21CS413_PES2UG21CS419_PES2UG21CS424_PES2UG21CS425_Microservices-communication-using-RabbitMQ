# producer/producer.py

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="item_queue")

    # Publish a message to the 'item_queue' queue
    channel.basic_publish(
        exchange="", routing_key="item_queue", body="New item added to inventory!"
    )
    print("Message sent to item_queue")
    connection.close()


if __name__ == "__main__":
    main()
