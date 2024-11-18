from bson import ObjectId
from flask import Blueprint, request, jsonify
from database import db
questions_bp = Blueprint('questions_bp', __name__)

# Routes for the 'questions' collection
@questions_bp.route('/questions', methods=['POST'])
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

@questions_bp.route('/questions', methods=['GET'])
def get_questions():
    questions = list(db.Questions.find())
    for question in questions:
        question["_id"] = str(question["_id"])
    return jsonify(questions)

@questions_bp.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    question = db.Questions.find_one({"_id": ObjectId(question_id)})
    if question:
        question["_id"] = str(question["_id"])
        return jsonify(question)
    return jsonify({"error": "Question not found"}), 404

@questions_bp.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if v is not None}
    result = db.Questions.update_one({"_id": ObjectId(question_id)}, {"$set": update_fields})
    return jsonify({"matched_count": result.matched_count}), 200 if result.matched_count else 404

@questions_bp.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    result = db.Questions.delete_one({"_id": ObjectId(question_id)})
    return jsonify({"deleted_count": result.deleted_count}), 200 if result.deleted_count else 404
