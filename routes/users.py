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


@users_bp.route('/users/<user_id>/update-decks', methods=['POST'])
def update_user_decks(user_id):
    data = request.json
    deck_ids = data.get("deck_ids", [])
    action = data.get("action", "add")  # Default action is 'add'

    if not deck_ids:
        return jsonify({"error": "No deck IDs provided"}), 400

    # Ensure all deck IDs are valid ObjectIds
    try:
        deck_ids = [ObjectId(deck_id) for deck_id in deck_ids]
    except:
        return jsonify({"error": "Invalid deck IDs"}), 400

    # Check if the user exists
    user = db.Users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    current_decks = set(user.get("decks", []))  # Use a set for efficient operations

    if action == "add":
        # Add decks (avoiding duplicates)
        updated_decks = current_decks.union({str(deck_id) for deck_id in deck_ids})
        message = "Decks added successfully"
    elif action == "remove":
        # Remove decks
        updated_decks = current_decks.difference({str(deck_id) for deck_id in deck_ids})
        message = "Decks removed successfully"
    else:
        return jsonify({"error": "Invalid action"}), 400

    # Update the user
    result = db.Users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"decks": list(updated_decks)}}
    )

    if result.modified_count:
        return jsonify({"message": message}), 200
    return jsonify({"message": "No changes made"}), 304


@users_bp.route('/users/<user_id>/decks', methods=['GET'])
def get_user_decks(user_id):
    # Fetch the user (optional, if needed for validation or logging)
    user = db.Users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Ensure the 'decks' field is a list
    deck_ids = user.get("decks", [])
    if not isinstance(deck_ids, list):
        return jsonify({"error": "Invalid deck data for user"}), 400

    # Convert deck_ids to ObjectId
    deck_object_ids = [ObjectId(deck_id) for deck_id in deck_ids]
    decks = list(db.Decks.find({"_id": {"$in": deck_object_ids}}))

    # Loop through each deck and fetch its associated questions
    for deck in decks:
        deck["_id"] = str(deck["_id"])
        question_ids = deck.get("questions", [])
        questions = list(db.Questions.find({"_id": {"$in": [ObjectId(q_id) for q_id in question_ids]}}))

        # Replace question_ids with the full question objects
        for question in questions:
            question["_id"] = str(question["_id"])

        deck["questions"] = questions

    # Return only the decks with their questions
    return jsonify(decks)
