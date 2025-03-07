import json
import os
import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "responses.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


def log_response(endpoint, request_data, response_data):
    """
    Logs request and response data to a file in JSON format.

    :param endpoint: API endpoint being accessed
    :param request_data: Data received in the request
    :param response_data: Response data to be logged
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "endpoint": endpoint,
        "request": request_data,
        "response": response_data
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"Logging error: {e}")
