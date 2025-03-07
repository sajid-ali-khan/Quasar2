import uuid

import google.generativeai as genai
import json

from flask import jsonify

from config import Config
from utils.log_util import log_response
from utils.json_utils import clean_json_response
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_path(data):
    skill = data.get("skill")
    level = data.get("level")
    goal = data.get("goal")
    duration_weeks = data.get("duration_weeks")
    estimated_hours = data.get("estimated_hours")  # From hrs_estimator

    if not all([skill, level, goal, duration_weeks, estimated_hours]):
        return jsonify({"error": "Missing required fields"}), 400

    roadmap_id = f"roadmap_{uuid.uuid4().hex[:8]}"
    course_id = f"course_{uuid.uuid4().hex[:8]}"

    prompt = f"""
    Create a structured weekly learning path for a user based on their skill level, learning goal, and estimated study hours.

    User Details:
    - Skill: {skill}
    - Self-assessed level: {level}
    - Learning goal: {goal}
    - Duration: {duration_weeks} weeks
    - Estimated total study hours: {estimated_hours}

    Format the response as a structured JSON:
    {{
      "roadmapId": "{roadmap_id}",
      "courseId": "{course_id}",
      "roadmapData": {{
        "week1": [
          {{
            "moduleId": "mod1",
            "title": "Module Title",
            "duration": "X days",
            "topics": [
              {{
                "topicId": "t1",
                "name": "Topic Name",
                "isComplete": false
              }}
            ]
          }}
        ]
      }}
    }}
    """

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text.strip("```json").strip("```").strip())
    except json.JSONDecodeError:
        return {"error": "Invalid response format"}