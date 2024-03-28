import pika
import time


def main():
    print("Healthcheck microservice running...")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        channel = connection.channel()
        channel.queue_declare(queue="item_queue")

        def callback(ch, method, properties, body):
            print("Received message:", body)

        channel.basic_consume(
            queue="item_queue", on_message_callback=callback, auto_ack=True
        )

        print("Waiting for messages...")
        channel.start_consuming()

    except Exception as e:
        print("Error occurred:", e)


if __name__ == "__main__":
    main()
