from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]  # Replace 'inventory_db' with your actual database name
collection = db["inventory"]  # Replace 'inventory' with your actual collection name


@app.route("/add_item", methods=["POST"])
def add_item():
    data = request.json
    if "name" not in data or "quantity" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_item = {"name": data["name"], "quantity": data["quantity"]}
    # Insert the new item into MongoDB
    result = collection.insert_one(new_item)

    # Include the inserted _id in the response
    new_item["_id"] = str(result.inserted_id)

    return jsonify(new_item), 201


@app.route("/inventory", methods=["GET"])
def get_inventory():
    inventory = list(collection.find({}))  # Retrieve all items from MongoDB
    # Convert ObjectId to string for serialization
    serialized_inventory = [{**item, "_id": str(item["_id"])} for item in inventory]
    return jsonify(serialized_inventory)


@app.route("/update_item/<item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    if "name" not in data or "quantity" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    updated_item = {"name": data["name"], "quantity": data["quantity"]}
    # Update the item in MongoDB
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item})

    if result.modified_count == 0:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item updated successfully"})


@app.route("/delete_item/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    # Delete the item from MongoDB
    result = collection.delete_one({"_id": ObjectId(item_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, jsonify, request
# from pymongo import MongoClient

# app = Flask(__name__)

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["inventory_db"]
# collection = db["inventory"]

# # Sample inventory data
# inventory = [
#     {"id": 1, "name": "Product 1", "quantity": 10},
#     {"id": 2, "name": "Product 2", "quantity": 20},
#     {"id": 3, "name": "Product 3", "quantity": 15},
# ]


# # Endpoint for health check
# @app.route("/health", methods=["GET"])
# def health_check():
#     return jsonify({"status": "OK"})


# # Endpoint to get all inventory items
# @app.route("/inventory", methods=["GET"])
# def get_inventory():
#     items = collection.find({})
#     return jsonify(list(items))


# # Endpoint to get a specific inventory item
# @app.route("/inventory/<int:item_id>", methods=["GET"])
# def get_item(item_id):
#     item = collection.find_one({"id": item_id})
#     if item:
#         return jsonify(item)
#     else:
#         return jsonify({"error": "Item not found"}), 404


# # Endpoint to add a new inventory item
# @app.route("/inventory", methods=["POST"])
# def add_item():
#     data = request.json
#     if "name" not in data or "quantity" not in data:
#         return jsonify({"error": "Missing required fields"}), 400
#     new_item = {"id": data["id"], "name": data["name"], "quantity": data["quantity"]}
#     collection.insert_one(new_item)
#     return jsonify(new_item), 201


# # Endpoint to update an existing inventory item
# @app.route("/inventory/<int:item_id>", methods=["PUT"])
# def update_item(item_id):
#     data = request.json
#     result = collection.update_one({"id": item_id}, {"$set": data})
#     if result.modified_count == 0:
#         return jsonify({"error": "Item not found"}), 404
#     else:
#         return jsonify({"message": "Item updated"}), 200


# # Endpoint to delete an inventory item
# @app.route("/inventory/<int:item_id>", methods=["DELETE"])
# def delete_item(item_id):
#     result = collection.delete_one({"id": item_id})
#     if result.deleted_count == 0:
#         return jsonify({"error": "Item not found"}), 404
#     else:
#         return jsonify({"message": "Item deleted"}), 200


# if __name__ == "__main__":
#     app.run(debug=True)
