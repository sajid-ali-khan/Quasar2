from config import Config
from flask import Flask, Request
import requests

app = Flask(__name__)

def search_article(topic_name):
    """Fetches the first article link related to the topic."""
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": Config.API_KEY,
        "cx": Config.SEARCH_ENGINE_ID,
        "q": topic_name
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    # Extract first relevant link
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["link"]
    return "No results found"

def get_youtube_link(topic_name):
    """Fetches the best YouTube video link related to the topic."""
    search_url = "https://www.googleapis.com/youtube/v3/search"

    # Try medium-length videos first
    durations = ["medium", "short"]

    for duration in durations:
        params = {
            "part": "snippet",
            "q": topic_name,
            "key": Config.YOUTUBE_API_KEY,
            "maxResults": 1,
            "type": "video",
            "videoDuration": duration,  # Try medium first, then short
            "order": "viewCount",  # Sort by most viewed

        }

        response = requests.get(search_url, params=params)
        data = response.json()

        if "items" in data and data["items"]:
            video_id = data["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"


