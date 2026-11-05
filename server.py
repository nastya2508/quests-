from datetime import datetime
import os
import csv
from flask import Flask, jsonify, request

app = Flask(__name__)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "inventory.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "category", "quantity", "price", "location", "created_at"])

def read_csv_data():
    items = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(row)
    return items

def write_csv_data(items):
    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "name", "category", "quantity", "price", "location", "created_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

@app.route("/items", methods=["GET"])
def get_items():
    items = read_csv_data()
    return jsonify(items), 200

@app.route("/items", methods=["POST"])
def add_item():
    data = request.json
    if not data or not data.get("name") or not data.get("price"):
        return jsonify({"error": "Невірні дані"}), 400

    try:
        quantity = int(data.get("quantity", 0))
        price = float(data.get("price", 0.0))
    except ValueError:
        return jsonify({"error": "Невірний тип даних"}), 400

    items = read_csv_data()
    
    if items:
        new_id = str(int(max(int(i["id"]) for i in items)) + 1)
    else:
        new_id = "1"

    new_row = {
        "id": new_id,
        "name": data["name"],
        "category": data.get("category", ""),
        "quantity": str(quantity),
        "price": str(price),
        "location": data.get("location", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    items.append(new_row)
    write_csv_data(items)
    return jsonify(new_row), 201

@app.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    items = read_csv_data()
    found = False

    for item in items:
        if item["id"] == str(item_id):
            item["name"] = data.get("name", item["name"])
            item["category"] = data.get("category", item["category"])
            try:
                item["quantity"] = str(int(data.get("quantity", item["quantity"])))
                item["price"] = str(float(data.get("price", item["price"])))
            except ValueError:
                return jsonify({"error": "Невірний формат"}), 400
            item["location"] = data.get("location", item["location"])
            found = True
            break

    if not found:
        return jsonify({"error": "Не знайдено"}), 404

    write_csv_data(items)
    return jsonify({"message": "Оновлено"}), 200

@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    items = read_csv_data()
    new_items = [i for i in items if i["id"] != str(item_id)]

    if len(new_items) == len(items):
        return jsonify({"error": "Не знайдено"}), 404

    write_csv_data(new_items)
    return jsonify({"message": "Видалено"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)