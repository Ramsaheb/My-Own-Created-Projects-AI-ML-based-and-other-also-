import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "mock") 
    API_URL = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"

    @classmethod
    def validate(cls):
        if not cls.HUGGINGFACE_TOKEN or cls.HUGGINGFACE_TOKEN.strip() == "":
            raise ValueError("HuggingFace token is required. Please check your .env file.")

