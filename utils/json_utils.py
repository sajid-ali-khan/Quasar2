import json
import re

def clean_json_response(response_text):
    try:
        # Extract JSON inside ```json ... ```
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL)

        if json_match:
            json_text = json_match.group(1)  # Extract JSON content
            return json.loads(json_text)  # Parse JSON
        else:
            return {"error": "No valid JSON found in response"}

    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {str(e)}"}
