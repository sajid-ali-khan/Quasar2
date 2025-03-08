import uuid

from flask import Blueprint, request, jsonify

from services.path_generator import generate_path
from services.quiz_generator import generate_questions
from services.quiz_evaluator import evaluate_quiz

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    skill = data.get("skill")
    level = data.get("level")
    goal = data.get("goal")

    if not skill:
        return jsonify({"error": "Missing required field: interested_skill"}), 400

    questions = generate_questions(skill, level, goal)
    return jsonify({"questions": questions})


@quiz_bp.route('/evaluate_quiz', methods=['POST'])
def evaluate_quiz_route():
    data = request.get_json()
    return evaluate_quiz(data)


@quiz_bp.route('/generate_path', methods=['POST'])
def path_generator():
    data = request.get_json()
    return generate_path(data)
