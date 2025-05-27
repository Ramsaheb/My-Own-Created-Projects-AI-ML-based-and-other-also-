from flask import Flask, jsonify, request
from flask_cors import CORS
from news_service import get_articles
from sentiment import analyze_sentiment
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Config.validate()

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://f4a135ce-f41c-493c-a2bb-e72585878747-00-2wjins3ibm4nv.sisko.replit.dev:3000",
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})



@app.route('/')
def home():
    return """
    <h1>News Sentiment Analysis API</h1>
    <p>Available endpoints:</p>
    <ul>
        <li>GET /api/articles?query=technology</li>
        <li>POST /api/analyze (with JSON {"text":"your text"})</li>
    </ul>
    <p>Frontend should be running on http://localhost:3000</p>
    """

@app.route('/api/articles', methods=['GET'])
def get_news():
    try:
        query = request.args.get('query', 'technology')
        logger.info(f"Fetching articles for query: {query}")
        articles = get_articles(query)
        return jsonify({
            "status": "success",
            "data": articles,
            "count": len(articles)
        })
    except Exception as e:
        logger.error(f"Error in get_news: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({"error": "Text parameter is required"}), 400

        logger.info(f"Analyzing sentiment for text: {text[:50]}...")
        result = analyze_sentiment(text)
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        logger.error(f"Error in analyze: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)