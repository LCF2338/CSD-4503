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
