from bson import ObjectId
from flask import Blueprint, request, jsonify
from database import db
main_routes = Blueprint('main_routes', __name__)

# Routes for the 'user' collection
@main_routes.route('/users', methods=['POST'])
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

@main_routes.route('/users', methods=['GET'])
def get_users():
    users = list(db.Users.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)

@main_routes.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.Users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@main_routes.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if v is not None}
    result = db.Users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
    return jsonify({"matched_count": result.matched_count}), 200 if result.matched_count else 404

@main_routes.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = db.Users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"deleted_count": result.deleted_count}), 200 if result.deleted_count else 404

# Routes for the 'deck' collection
@main_routes.route('/decks', methods=['POST'])
def create_deck():
    data = request.json
    deck = {
        "name": data.get("name"),
        "time_to_complete": data.get("time_to_complete"),
        "questions": data.get("questions", [])
    }
    result = db.Decks.insert_one(deck)
    return jsonify({"_id": str(result.inserted_id)}), 201

@main_routes.route('/decks', methods=['GET'])
def get_decks():
    decks = list(db.Decks.find())
    for deck in decks:
        deck["_id"] = str(deck["_id"])
    return jsonify(decks)

@main_routes.route('/decks/<deck_id>', methods=['GET'])
def get_deck(deck_id):
    deck = db.Decks.find_one({"_id": ObjectId(deck_id)})
    if deck:
        deck["_id"] = str(deck["_id"])
        return jsonify(deck)
    return jsonify({"error": "Deck not found"}), 404

@main_routes.route('/decks/<deck_id>', methods=['PUT'])
def update_deck(deck_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if v is not None}
    result = db.Decks.update_one({"_id": ObjectId(deck_id)}, {"$set": update_fields})
    return jsonify({"matched_count": result.matched_count}), 200 if result.matched_count else 404

@main_routes.route('/decks/<deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    result = db.Decks.delete_one({"_id": ObjectId(deck_id)})
    return jsonify({"deleted_count": result.deleted_count}), 200 if result.deleted_count else 404

# Routes for the 'questions' collection
@main_routes.route('/questions', methods=['POST'])
def create_question():
    data = request.json
    question = {
        "question_text": data.get("question_text"),
        "question_answer": data.get("question_answer"),
        "question_img": data.get("question_img"),
        "difficulty": data.get("difficulty")
    }
    result = db.Questions.insert_one(question)
    return jsonify({"_id": str(result.inserted_id)}), 201

@main_routes.route('/questions', methods=['GET'])
def get_questions():
    questions = list(db.Questions.find())
    for question in questions:
        question["_id"] = str(question["_id"])
    return jsonify(questions)

@main_routes.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    question = db.Questions.find_one({"_id": ObjectId(question_id)})
    if question:
        question["_id"] = str(question["_id"])
        return jsonify(question)
    return jsonify({"error": "Question not found"}), 404

@main_routes.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if v is not None}
    result = db.Questions.update_one({"_id": ObjectId(question_id)}, {"$set": update_fields})
    return jsonify({"matched_count": result.matched_count}), 200 if result.matched_count else 404

@main_routes.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    result = db.Questions.delete_one({"_id": ObjectId(question_id)})
    return jsonify({"deleted_count": result.deleted_count}), 200 if result.deleted_count else 404
