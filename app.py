import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" for simplicity. Swap for Postgres later if you want.
ITEMS = [
    {"id": 1, "name": "Docker"},
    {"id": 2, "name": "Kubernetes"},
    {"id": 3, "name": "Terraform"},
]


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the DevOps demo API"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(ITEMS), 200


@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "name field is required"}), 400

    new_item = {"id": len(ITEMS) + 1, "name": data["name"]}
    ITEMS.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
