from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "Itemdata.json"

def load_items():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("JSON Load Error:", e)
        return []

@app.route("/")
def home():
    return {"status": "API running"}

@app.route("/info")
def get_item():
    item_id = request.args.get("item_id")

    if not item_id:
        return jsonify({"error": "item_id required"}), 400

    try:
        item_id = int(item_id)
    except:
        return jsonify({"error": "item_id must be number"}), 400

    items = load_items()

    for item in items:
        if item.get("itemID") == item_id:
            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)