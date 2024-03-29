# PES2UG21CS413_PES2UG21CS419_PES2UG21CS424_PES2UG21CS425_Microservices-communication-using-RabbitMQ


run : docker-compose up --build

producer:
Flask application that acts as a producer for a RabbitMQ message queue.
It exposes several HTTP endpoints to perform CRUD (Create, Read, Update, Delete) operations and healthcheck on an inventory system.

consumer:
Consumes the messages from the RabbitMQ message queue and performs the operations

1. consumer_one    will check the mangoDB and RabbitMQ connections.

  GET http://127.0.0.1:8000/health_check


2. consumer_two    will create the document in the MongoDB database named inventory_db in the collection inventory.

  POST http://127.0.0.1:8000/create_item

  body
  {
    "product_id": "1",
    "name": "Ram",
    "quantity": 1000,
    "price": 10.99,
    "description": "This is an MF product."
  }


3. consumer_three  will update the document with requested product_id in the MongoDB database named inventory_db in the collection     inventory.

  PUT http://127.0.0.1:8000/update_item/<product_id>

  body
  {
      "name": "Ram",
      "quantity": 2000,
      "price": 19.99,
      "description": "This is an updated MF product."
  }


4. consumer_four   will read all the documents in the MongoDB database named inventory_db in the collection inventory.

  GET http://127.0.0.1:8000/read_items


5. consumer_five   will delete the document with requested product_id in the MongoDB database named inventory_db in the collection inventory.

  DELETE http://127.0.0.1:8000/delete_item/<product_id>


