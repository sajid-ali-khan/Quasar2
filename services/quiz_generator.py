import google.generativeai as genai
import json
from config import Config
from utils.json_utils import clean_json_response

genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_questions(skill, level, goal):
    prompt = f"""
    You are an expert in personalized learning assessment. Generate 10 multiple-choice questions in JSON format.

    - Each question should have exactly 4 short options (under 5 words).
    - No answers, just questions and options.

    Output format:
    ```json
    [
      {{"id": 1, "question": "What is AI?", "options": ["Machine learning", "A software", "Physics concept", "Algorithm"]}},
      {{"id": 2, "question": "Use of cloud computing?", "options": ["Data storage", "Cooking", "Car repair", "Gardening"]}}
    ]
    ```

    User's input:
    "interested_skill": "{skill}",
    "self_assessed_level": "{level}",
    "goal": "{goal}"
    """

    response = model.generate_content(prompt)
    print(response)
    try:
        return clean_json_response(response.text)
    except json.JSONDecodeError:
        return {"error": "Invalid response format"}
