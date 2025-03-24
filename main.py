import os
import sys
from news_processor import NewsProcessor, OpenAIProcessor, GeminiProcessor, Article
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Load environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize FastAPI app
app = FastAPI(title="Neutral News API",
             description="An API for fetching and processing news articles for neutrality",
             version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
ai_processors = [
    OpenAIProcessor(OPENAI_API_KEY),
    GeminiProcessor(GEMINI_API_KEY)
]

# Initialize news processor
news_processor = NewsProcessor(NEWS_API_KEY, ai_processors)

class ArticleResponse(BaseModel):
    title: str
    content: str
    author: str
    description: str
    url: str
    published_at: str
    source_name: str
    category: str
    fact_check_status: str

@app.get("/news/", response_model=List[ArticleResponse])
async def get_news(
    country: str = "us",
    category: Optional[str] = None,
    page_size: int = 10
):
    try:
        articles = news_processor.fetch_news(country, category, page_size)
        processed_articles = []
        
        for article in articles:
            processed_article = news_processor.process_article(article)
            processed_articles.append(processed_article)
            
        return processed_articles
    except Exception as e:
        logging.error(f"Error processing news request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/{article_url:path}", response_model=ArticleResponse)
async def get_article(article_url: str):
    try:
        # Fetch single article by URL
        articles = news_processor.fetch_news(page_size=100)
        article = next((a for a in articles if a.url == article_url), None)
        
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
            
        processed_article = news_processor.process_article(article)
        return processed_article
    except Exception as e:
        logging.error(f"Error processing article request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)