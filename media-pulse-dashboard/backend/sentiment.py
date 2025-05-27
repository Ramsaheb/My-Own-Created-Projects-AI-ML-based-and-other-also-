import requests
from config import Config

def analyze_sentiment(text):
    if not text.strip():
        return {"error": "No text provided"}

    try:
        response = requests.post(
            Config.API_URL,
            headers={"Authorization": f"Bearer {Config.HUGGINGFACE_TOKEN}"},
            json={"inputs": text[:512]}
        )
        if response.status_code != 200:
            return {"error": f"API error {response.status_code}", "details": response.text}

        result = response.json()
        return {
            "sentiment": result[0][0]["label"],
            "confidence": result[0][0]["score"]
        }
    except Exception as e:
        return {"error": str(e)}
