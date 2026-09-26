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


def generate_article(title, summary, link):
    prompt = f"""
    Escreva uma notícia original em português do Brasil.
    Use somente as informações fornecidas.
    Não invente fatos, datas ou declarações.
    Não copie o texto da fonte.
    Informe que o conteúdo é um resumo baseado na fonte.
    Crie um título e um texto informativo.
    Inclua o link da fonte ao final.

    Título: {title}
    Resumo: {summary}
    Fonte: {link}
    """

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        },
        timeout=90,
    )
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def publish_to_blogger(title, content, token):
    url = (
        f"https://www.googleapis.com/blogger/v3/blogs/"
        f"{BLOG_ID}/posts/"
    )

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        params={"isDraft": "true"},
        json={
            "kind": "blogger#post",
            "title": title,
            "content": content,
        },
        timeout=30,
    )
    response.raise_for_status()
    print("Rascunho criado:", title)


def main():
    feed = feedparser.parse(RSS_URL)
    token = get_access_token()

    for item in feed.entries[:3]:
        title = item.get("title", "")
        summary = item.get("summary", "")
        link = item.get("link", "")

        if not title or not link:
            continue

        article = generate_article(title, summary, link)
        publish_to_blogger(title, article, token)


if __name__ == "__main__":
    main()
