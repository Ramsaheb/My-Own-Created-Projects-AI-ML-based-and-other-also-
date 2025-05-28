import requests
import logging
import re
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_sentiment(article):
    """Enhanced sentiment analysis with better context handling"""
    if not article.get('title'):
        return {"error": "Invalid article format"}

    # Preprocess text - combine title and description with cleaning
    text = f"{article['title']}. {article.get('description', '')}"
    text = re.sub(r'\s+', ' ', text).strip()

    if not text:
        return {"sentiment": "neutral", "confidence": 0.0}

    try:
        payload = {
            "inputs": text[:1000],
            "parameters": {
                "return_all_scores": True,
                "truncation": True
            }
        }

        headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_TOKEN}"}
        response = requests.post(
            "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        result = response.json()

        scores = result[0] if isinstance(result, list) else result

        max_score = max(scores, key=lambda x: x['score'])
        sentiment = max_score['label'].lower()

        if max_score['score'] < 0.6:
            return {"sentiment": "neutral", "confidence": max_score['score']}

        return {
            "sentiment": sentiment,
            "confidence": max_score['score']
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Sentiment API error: {e}")
        return {"sentiment": "neutral", "confidence": 0.0}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"sentiment": "neutral", "confidence": 0.0}
