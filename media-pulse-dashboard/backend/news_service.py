import json
import os
import requests
from config import Config

def _get_mock_articles(query):
    """Load mock articles from local file mock_articles.json"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mock_path = os.path.join(dir_path, 'mock_articles.json')

    try:
        with open(mock_path, encoding='utf-8') as f:
            articles = json.load(f)
        return [a for a in articles if query.lower() in a['title'].lower()][:3]
    except Exception as e:
        print(f"Mock load failed: {e}")
        return [{
            'title': f"Mock article about {query}",
            'description': "Sample description",
            'url': "#",
            'source': "Mock News",
            'publishedAt': "2023-01-01T00:00:00Z"
        }]

def get_articles(query):
    if Config.NEWSAPI_KEY == 'mock':
        return _get_mock_articles(query)

    try:
        url = f"https://newsapi.org/v2/everything?q={query}&pageSize=5&apiKey={Config.NEWSAPI_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error on bad status
        articles = response.json().get('articles', [])
        return [{
            'title': a.get('title', 'No title'),
            'description': a.get('description', ''),
            'url': a.get('url', '#'),
            'source': a.get('source', {}).get('name', 'Unknown'),
            'publishedAt': a.get('publishedAt', '')
        } for a in articles[:5]]
    except Exception as e:
        print(f"News API failed: {e}")
        return _get_mock_articles(query)
