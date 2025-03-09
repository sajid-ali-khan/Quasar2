import uuid

import google.generativeai as genai
import json

from flask import jsonify

from config import Config
from utils.log_util import log_response
from utils.json_utils import clean_json_response
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_modules_with_weeks(roadmap_data):
    modules_with_weeks = []
    print(roadmap_data)
    for entry in roadmap_data:
        week = entry["week"]
        for module in entry["modules"]:
            modules_with_weeks.append({
                "week": week,
                "moduleId": module["moduleId"],
                "title": module["title"],
                "topics": module["topics"],
            })
    return modules_with_weeks

def generate_path(data):
    skill = data.get("skill")
    level = data.get("level")
    goal = data.get("goal")
    duration_weeks = data.get("duration_weeks")
    estimated_hours = data.get("estimated_hours")

    if not all([skill, level, goal, duration_weeks, estimated_hours]):
        return jsonify({"error": "Missing required fields"}), 400

    roadmap_id = f"roadmap_{uuid.uuid4().hex[:8]}"
    course_id = f"course_{uuid.uuid4().hex[:8]}"

    prompt = """
    ### **ROLE ASSIGNMENT:**
You are an **AI Learning Path Expert**, specializing in generating structured JSON roadmaps for students. Your task is to create a **weekly learning roadmap** based on user details, skill levels, and assessment data.

Your expertise includes:
- Structuring **weekly study plans** tailored to the user's available time.
- **Evenly distributing learning modules** over `{duration_weeks}` weeks.
- **Excluding topics the user already knows** (based on assessment results).
- Outputting **strictly valid JSON** without any additional text.

---

### **INPUT DETAILS:**
**User Information:**
- Skill: {skill}
- Self-assessed level: {level}
- Learning Goal: {goal}
- Duration: {duration_weeks} weeks
- Estimated Total Study Hours: {estimated_hours}

**User Assessment Data:**
- Test Questions with 4 Options Each: {questions}
- Selected Options: {selected_options}

---

### **Roadmap Generation Rules:**

1. **STRICT WEEK DISTRIBUTION**  
   - The roadmap must be divided **exactly** into `{duration_weeks}` weeks.  
   - Topics and modules **must be evenly distributed** across the given weeks.  
   - No week should have too many or too few topics—maintain a balanced workload.  

2. **Adaptive Learning**  
   - **Exclude topics** that the user already knows (correctly answered in the test).  
   - Prioritize **weaker** areas to maximize learning effectiveness.  

3. **Global Identifiers**  
   - Each `moduleId`, `topicId`, and `week` must be **globally unique**.  

4. **STRICT JSON OUTPUT RULES:**  
   - The output must be **valid JSON**, with **double quotes ("")** around all keys and values.  
   - Do **NOT** include explanations, comments, or extra text.  
   - Use correct **nesting and indentation** for JSON objects.  

---
this is for mat for one week 
### **OUTPUT FORMAT (STRICTLY FOLLOW THIS STRUCTURE):**
```json
{{
  "roadmapId": "{roadmap_id}",
  "courseId": "{course_id}",
  "courseName": <a relevant course name based on data>,
  "category": <a category name based on course>,
  "duration": <estimated_hours>,
  "remaining": < >,
  "roadmapData": [
    {{
      "week": 1,
      "modules": [
        {{
          "moduleId": "{module_id_1}",
          "title": "{module_title_1}",
          "topics": [
            {{
              "topicId": "{topic_id_1}",
              "name": "{topic_name_1}",
              "isComplete": false
            }},
            {{
              "topicId": "{topic_id_2}",
              "name": "{topic_name_2}",
              "isComplete": false
            }}
          ]
        }},
        {{
          "moduleId": "{module_id_2}",
          "title": "{module_title_2}",
          "topics": [
            {{
              "topicId": "{topic_id_3}",
              "name": "{topic_name_3}",
              "isComplete": false
            }}
          ]
        }}
      ]
    }},
    
  ]
}}

    """

    response = model.generate_content(prompt)
    print(response.text)
    try:
        return clean_json_response(response.text)
    except json.JSONDecodeError:
        return {"error": "Invalid response format"}