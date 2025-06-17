from langchain.tools import tool
from newsapi import NewsApiClient
import os

@tool
def get_latest_news(topic: str) -> str:
    """Get the latest English-language news headlines for a given topic."""
    newsapi = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])
    articles = newsapi.get_everything(
        q=topic,
        sort_by="publishedAt",
        page_size=3,
        language="en",     # Only English
        domains="bbc.com,cnn.com,nytimes.com,techcrunch.com"  # Optional: trusted sources
    )

    if not articles["articles"]:
        return "No recent news found."

    return "\n\n".join([f"{a['title']}\n{a['description']}" for a in articles["articles"]])



from langchain.tools import tool
import wikipedia

@tool
def get_wikipedia_summary(topic: str) -> str:
    """Get a short summary of a topic from Wikipedia, defaulting to company if ambiguous."""
    import wikipedia
    try:
        # Try to handle ambiguity (Tesla → Tesla, Inc.)
        if topic.lower() == "tesla":
            topic = "Tesla, Inc."

        return wikipedia.summary(topic, sentences=3)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Too many meanings. Try one of: {', '.join(e.options[:5])}"
    except Exception as e:
        return f"No summary found. Error: {str(e)}"
