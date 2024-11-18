from bson import ObjectId
from flask import Blueprint, request, jsonify
from database import db
decks_bp = Blueprint('decks_bp', __name__)

# Routes for the 'deck' collection
@decks_bp.route('/decks', methods=['POST'])
def create_deck():
    data = request.json
    deck = {
        "name": data.get("name"),
        "time_to_complete": data.get("time_to_complete"),
        "questions": data.get("questions", [])
    }
    result = db.Decks.insert_one(deck)
    return jsonify({"_id": str(result.inserted_id)}), 201

@decks_bp.route('/decks', methods=['GET'])
def get_decks():
    decks = list(db.Decks.find())
    for deck in decks:
        deck["_id"] = str(deck["_id"])
    return jsonify(decks)

@decks_bp.route('/decks/<deck_id>', methods=['GET'])
def get_deck(deck_id):
    deck = db.Decks.find_one({"_id": ObjectId(deck_id)})
    if deck:
        deck["_id"] = str(deck["_id"])
        question_ids = deck.get("questions", [])
        questions = list(db.Questions.find({"_id": {"$in": [ObjectId(q_id) for q_id in question_ids]}}))
        # Convert each question's _id to string
        for question in questions:
            question["_id"] = str(question["_id"])
        # Replace question_ids with full question objects
        deck["questions"] = questions
        return jsonify(deck)
    return jsonify({"error": "Deck not found"}), 404

@decks_bp.route('/decks/<deck_id>', methods=['PUT'])
def update_deck(deck_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if v is not None}
    result = db.Decks.update_one({"_id": ObjectId(deck_id)}, {"$set": update_fields})
    return jsonify({"matched_count": result.matched_count}), 200 if result.matched_count else 404

@decks_bp.route('/decks/<deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    result = db.Decks.delete_one({"_id": ObjectId(deck_id)})
    return jsonify({"deleted_count": result.deleted_count}), 200 if result.deleted_count else 404


@decks_bp.route('/decks/<deck_id>/update-questions', methods=['POST'])
def modify_questions_in_deck(deck_id):
    data = request.json
    question_ids = data.get("question_ids", [])
    action = data.get("action", "add")  # Default action is 'add'

    if not question_ids:
        return jsonify({"error": "No question IDs provided"}), 400

    # Ensure all question IDs are valid ObjectIds
    try:
        question_ids = [ObjectId(q_id) for q_id in question_ids]
    except:
        return jsonify({"error": "Invalid question IDs"}), 400

    # Check if the deck exists
    deck = db.Decks.find_one({"_id": ObjectId(deck_id)})
    if not deck:
        return jsonify({"error": "Deck not found"}), 404

    current_questions = set(deck.get("questions", []))  # Use a set for efficient operations

    if action == "add":
        # Add questions (avoiding duplicates)
        updated_questions = current_questions.union({str(q_id) for q_id in question_ids})
        message = "Questions added successfully"
    elif action == "remove":
        # Remove questions
        updated_questions = current_questions.difference({str(q_id) for q_id in question_ids})
        message = "Questions removed successfully"
    else:
        return jsonify({"error": "Invalid action"}), 400

    # Update the deck
    result = db.Decks.update_one(
        {"_id": ObjectId(deck_id)},
        {"$set": {"questions": list(updated_questions)}}
    )

    if result.modified_count:
        return jsonify({"message": message}), 200
    return jsonify({"message": "No changes made"}), 304
