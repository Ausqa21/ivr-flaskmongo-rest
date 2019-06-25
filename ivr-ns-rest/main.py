from flask import Blueprint, request, jsonify
from .extensions import mongo
from flask_argon2 import Argon2
import json
from bson.objectid import ObjectId
from .schema import validate_user_data


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)


main = Blueprint("main", __name__)

main.json_encoder = JSONEncoder

argon_two = Argon2(main)


# Home/Index
@main.route("/", methods=["GET"])
def index():
    return "<h1>We ouchea!</h1>"


# Check if user exists [EXCEPTION HANDLING]
@main.route("/check/<number>", methods=["GET"])
def check_user(number):
    user_collection = mongo.db.users
    if user_collection.find_one({"number": number}):
        return jsonify({"is_user": True})
    else:
        return jsonify({"is_user": False})


# Get a user [EXCEPTION HANDLING]
@main.route("/user/<number>", methods=["POST"])
def get_user(number):
    user_data = request.get_json()
    user_collection = mongo.db.users
    user = user_collection.find_one({"number": number})
    if user:
        if argon_two.check_password_hash(user["passcode"], user_data["passcode"]):
            return jsonify(user), 200
        else:
            return jsonify({"ok": False, "message": "Check your inputs and try again"}), 400
    else:
        return jsonify({"ok": False, "message": f"User {number} does not exist"})

# Get all users
@main.route("/users", methods=["GET"])
def get_all_users():
    user_collection = mongo.db.users.find()
    user_list = []
    for user in user_collection:
        user_list.append(user)
    return jsonify(user_list)


# Create a user
@main.route("/create", methods=["POST"])
def create_user():
    user_data = validate_user_data(request.get_json())
    if user_data["ok"]:
        data = user_data["data"]
        user_collection = mongo.db.users

        data["passcode"] = argon_two.generate_password_hash(data["passcode"])
        user_collection.insert_one(data)
        return jsonify({"ok": True, "message": "User created successfully."}), 200
    else:
        return jsonify({"ok": False, "message": f"Bad request parameters: {user_data['message']}"}), 400


# Update a user
@main.route("/user/update", methods=["PATCH"])
def update_user():
    user_data = request.get_json()
    if user_data["payload"]["passcode"]:
        passcode = argon_two.generate_password_hash(user_data["payload"]["passcode"])
        user_data["payload"]["passcode"] = passcode
    user_collection = mongo.db.users
    if user_data.get("query", {}) != {}:
        user_collection.update_one(user_data["query"], {"$set": user_data.get("payload", {})})
    return jsonify(user_data)
