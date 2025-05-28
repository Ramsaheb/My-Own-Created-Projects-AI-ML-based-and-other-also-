import json
import os
import requests
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _create_fallback_article(query):
    return [{
        'title': f"Article about {query}",
        'description': "Sample description",
        'content': "Fallback content",
        'url': "#",
        'source': "Fallback News",
        'publishedAt': "2023-01-01T00:00:00Z"
    }]

def _get_mock_articles(query):
    """Load mock articles with improved relevance filtering"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mock_path = os.path.join(dir_path, 'mock_articles.json')

    try:
        with open(mock_path, encoding='utf-8') as f:
            articles = json.load(f)

        # Enhanced relevance scoring
        filtered = []
        for a in articles:
            score = 0
            title = a.get('title', '').lower()
            content = a.get('content', '').lower()

            if query.lower() in title:
                score += 2
            if query.lower() in content:
                score += 1

            if score > 0:
                filtered.append((a, score))

        # Sort by relevance and date
        filtered.sort(key=lambda x: (-x[1], x[0]['publishedAt']), reverse=True)
        return [a[0] for a in filtered[:5]]

    except Exception as e:
        logger.error(f"Mock load failed: {e}")
        logger.info("Using fallback article due to mock load failure.")
        return _create_fallback_article(query)

def get_articles(query):
    if getattr(Config, 'NEWSAPI_KEY', 'mock') == 'mock':
        return _get_mock_articles(query)

    try:
        url = f"https://newsapi.org/v2/everything?q={query}&pageSize=10&apiKey={Config.NEWSAPI_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        articles = response.json().get('articles', [])

        # Enhanced relevance filtering with content check
        filtered = []
        for a in articles:
            text_fields = [
                a.get('title', ''),
                a.get('description', ''),
                a.get('content', '')[:200]
            ]
            if any(query.lower() in (tf or '').lower() for tf in text_fields):
                filtered.append(a)

        # Process and limit results
        return [{
            'title': a.get('title', 'No title').strip(),
            'description': a.get('description', '').strip(),
            'content': a.get('content', '')[:500],
            'url': a.get('url', '#'),
            'source': a.get('source', {}).get('name', 'Unknown'),
            'publishedAt': a.get('publishedAt', '')
        } for a in filtered[:5]]

    except Exception as e:
        logger.error(f"News API failed: {e}")
        logger.info("Using fallback article due to News API failure.")
        return _get_mock_articles(query)
