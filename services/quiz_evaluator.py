from logging import error

import google.generativeai as genai
import json

from flask import jsonify

from config import Config
from utils.log_util import log_response
from utils.json_utils import clean_json_response
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def evaluate_quiz(data):
    """
    Evaluates quiz responses and estimates mastery time.
    """
    questions = data.get("questions", [])
    selected_options = data.get("selected_options", [])
    skill = data.get("skill")
    level = data.get("level")
    goal = data.get("goal")

    # Validation
    if not skill or not level or not goal:
        return jsonify({"error": "Missing required fields: skill, level, or goal"}), 400
    if not questions or not selected_options:
        return jsonify({"error": "Missing questions or selected options"}), 400
    if len(questions) != len(selected_options):
        return jsonify({"error": "Mismatch between number of questions and selected options"}), 400

    # AI Prompt
    prompt = f"""
You are an AI expert in personalized learning assessment. Your task is to generate **10 multiple-choice questions** in valid JSON format.  

### **Rules for Question Generation:**
1. Each question must have **exactly 4 short options** (under 5 words each).  
2. **No explanations, comments, or metadata**—only pure JSON output.  
3. The output **must be a valid JSON array** enclosed within square brackets (`[` and `]`).  
4. **DO NOT include triple backticks (` ```json `) or Markdown formatting**.  
5. Questions should be **relevant** to:
   - Skill: {skill}
   - Self-assessed level: {level}
   - Goal: {goal}

### **OUTPUT FORMAT (STRICTLY FOLLOW THIS STRUCTURE):**
```json
[
  {{"id": 1, "question": "What is AI?", "options": ["Machine learning", "A software", "Physics concept", "Algorithm"]}},
  {{"id": 2, "question": "Use of cloud computing?", "options": ["Data storage", "Cooking", "Car repair", "Gardening"]}}
]

    """

    response = model.generate_content(prompt)

    try:
        return clean_json_response(response.text)
    except error as e:
        print(e)
        return {"error": "Invalid response format", "actual": e}
