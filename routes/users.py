from bson import ObjectId
from flask import Blueprint, request, jsonify
from database import db
users_bp = Blueprint('users_bp', __name__)

# Routes for the 'user' collection
@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = {
        "name": data.get("name"),
        "email": data.get("email"),
        "password": data.get("password"),
        "decks": data.get("decks", [])
    }
    result = db.Users.insert_one(user)
    return jsonify({"_id": str(result.inserted_id)}), 201

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = list(db.Users.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.Users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if v is not None}
    result = db.Users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
    return jsonify({"matched_count": result.matched_count}), 200 if result.matched_count else 404

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = db.Users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"deleted_count": result.deleted_count}), 200 if result.deleted_count else 404
