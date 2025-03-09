from flask import Blueprint, jsonify
from services.resource_service import search_article, get_youtube_link

res_bp = Blueprint('resource', __name__)

@res_bp.get('/article/<topic>')
def getTopicArticle(topic):
    if not topic:
        return jsonify({"error": "Topic is empty"}), 400
    return jsonify({"article_link": search_article(topic)})

@res_bp.get('/video/<topic>')
def getTopicVideo(topic):
    if not topic:
        return jsonify({"error": "Topic is empty"}), 400
    return jsonify({"video_link": get_youtube_link(topic)})
