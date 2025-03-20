import requests
import json
from chat_processor import chat_with_openai
from chat_processor import revised_article

url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=4af7d24c8b3f4cf58892f8ebe4a6b99f')

response = requests.get(url)



if response.status_code == 200:
    articles = response.json()

    if 'articles' in articles:
        print(f"Total number of articles: {len(articles['articles'])}")
    
    if 'articles' in articles and len(articles['articles']) > 1:
        article_1 = articles['articles'][11]
        
        art = {
            'title': article_1.get('title', ''),
            'content': article_1.get('content', ''),
            'author': article_1.get('author', ''),
            'description': article_1.get('description', '')
        }
        
        arty = " ".join(filter(None, art.values()))
        
        neutral_news = revised_article(arty)
        print(neutral_news)
    else:
        print("No sufficient articles found.")
else:
    print(f"Failed to fetch news articles. Status code: {response.status_code}")
