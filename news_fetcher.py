import requests

def fetch_news(sources: list):
    news_articles = []
    for source in sources:
        # Example API call to fetch news from a source
        response = requests.get(f"https://newsapi.org/v2/everything?sources={source}&apiKey=YOUR_API_KEY")
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            for article in articles:
                news_articles.append({
                    "source": source,
                    "title": article.get("title"),
                    "content": article.get("content")
                })
        else:
            raise Exception(f"Failed to fetch news from source: {source}")
    return news_articles