from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Configure MongoDB client and database
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json()
    collection.insert_one(data)
    return "Record inserted successfully"

@app.route("/fetch", methods=["GET"])
def fetch():
    data = []
    for doc in collection.find():
        data.append(doc)
    return jsonify(data)
