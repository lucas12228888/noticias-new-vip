import os
import requests
import feedparser
from datetime import datetime, timezone

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
BLOG_ID = os.environ["BLOG_ID"]
CLIENT_ID = os.environ["BLOGGER_CLIENT_ID"]
CLIENT_SECRET = os.environ["BLOGGER_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["BLOGGER_REFRESH_TOKEN"]

RSS_URL = (
    "https://news.google.com/rss"
    "?hl=pt-BR&gl=BR&ceid=BR:pt-419"
)

def get_access_token():
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    
    if response.status_code != 200:
        print(f"OAuth Error: {response.status_code}")
        print(f"Response: {response.text}")
        
    response.raise_for_status()
    return response.json()["access_token"]

def main():
    print("A obter token de acesso...")
    token = get_access_token()
    print("Token obtido com sucesso!")
    
    # Restante da lógica de publicação...

if __name__ == "__main__":
    main()
