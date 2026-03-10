from flask import Flask, request, jsonify, send_file
import os
import json
import requests
from io import BytesIO
from PIL import Image

app = Flask(__name__)

JSON_FILE = "Itemdata.json"

def load_items():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("JSON Load Error:", e)
        return []

items = load_items()


@app.route("/")
def home():
    return {"status": "API running"}


# ITEM INFO
@app.route("/info", methods=["GET"])
def get_item_info():
    item_id = request.args.get("item_id")

    if not item_id:
        return jsonify({"error": "item_id required"}), 400

    try:
        item_id = int(item_id)
    except:
        return jsonify({"error": "item_id must be number"}), 400

    for item in items:
        if item.get("itemID") == item_id:
            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


# ITEM ICON
@app.route("/icon", methods=["GET"])
def get_item_icon():
    item_id = request.args.get("item_id")

    if not item_id:
        return jsonify({"error": "item_id required"}), 400

    try:
        item_id = int(item_id)
    except:
        return jsonify({"error": "item_id must be number"}), 400

    item = next((i for i in items if i.get("itemID") == item_id), None)

    if not item or not item.get("icon"):
        return jsonify({"error": "Item or icon not found"}), 404

    icon_name = item["icon"]
    image_url = f"https://freefiremobile-a.akamaihd.net/common/Local/PK/FF_UI_Icon/{icon_name}.png"

    response = requests.get(image_url)
    if response.status_code != 200:
        return jsonify({"error": "Icon image not found"}), 404

    img = Image.open(BytesIO(response.content))
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5019, debug=True)
