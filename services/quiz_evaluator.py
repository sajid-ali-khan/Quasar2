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
    You are an AI assistant designed to estimate the total number of **hours** a user needs to learn a skill, based on their **quiz performance, prior knowledge, and learning goal**.

    ### **Learning Constraints:**
    - The user can dedicate **6 to 9 hours per week**.
    - The **maximum duration is 12 weeks** (72 to 108 hours total).
    - The estimated time should be **within this range**.

    ### **User Information:**
    - **Skill:** {skill}
    - **Self-assessed level:** {level}
    - **Learning goal:** {goal}`

    ### **Quiz Details:**
    - Below are the **questions and answer choices**:
      {json.dumps(questions, indent=2)}
    - Below are the user's selected answers with question index according to above questions sequence(if "" for any question index the question is skipped by user)**:
      {json.dumps(selected_options, indent=2)}

    ### **Task:**
    1. **Analyze** the difficulty of the skill.
    2. **Evaluate** the user's quiz performance.
    3. **Adjust** learning time based on:
       - The skill's complexity.
       - The user's quiz accuracy.
       - Their prior knowledge (based on self-assessed level).
       - The depth of the learning goal (basic vs. advanced).
    4. **Ensure** the estimated time falls within **72 to 108 hours**.

    ### **Output Format:**  
    Provide the estimated learning time in **valid JSON format only** with no extra text, explanations, or comments.

    ```json
    {{
        "estimated_time": <integer>
    }}
    ```
    """

    response = model.generate_content(prompt)

    try:
        result = json.loads(response.text.strip("```json").strip("```").strip())
        return result
    except error as e:
        print(e)
        return {"error": "Invalid response format", "actual": e}
