def mock_wikipedia_summary(query: str) -> str:
    # Simulate API output
    return f"(Mock Wikipedia Summary) Key facts about: {query}."


import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Ensure it's in your .env file

def get_news_summary(query: str, from_date: str = "2025-05-12") -> str:
    url = (
        f"https://newsapi.org/v2/everything?q={query}&from={from_date}"
        f"&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "articles" not in data:
        return f"No news found or API error: {data.get('message', 'Unknown error')}"

    articles = data["articles"][:3]  # Limit to top 3 articles
    news_summary = "\n\n".join(
        f"🔹 {article['title']}\n{article['description'] or 'No description'}"
        for article in articles
    )
    return f"📰 Top News for '{query}':\n\n{news_summary}"
