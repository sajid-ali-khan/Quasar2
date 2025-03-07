import json

def clean_json_response(response_text):
    try:
        return json.loads(response_text.strip("```json").strip("```").strip())
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
