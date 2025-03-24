import requests
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='news_processor.log'
)
logger = logging.getLogger(__name__)

@dataclass
class Article:
    title: str
    content: str
    author: str
    description: str
    url: str
    published_at: datetime
    source_name: str
    category: str
    sentiment_score: float = 0.0
    fact_check_status: str = "pending"
    
class NewsAPIConfig:
    BASE_URL = "https://newsapi.org/v2"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def get_headers(self) -> Dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

class AIProcessor(ABC):
    @abstractmethod
    def analyze_content(self, text: str) -> str:
        pass
    
    @abstractmethod
    def fact_check(self, claims: List[str]) -> Dict[str, bool]:
        pass

class OpenAIProcessor(AIProcessor):
    def __init__(self, api_key: str):
        import openai
        self.client = openai
        self.client.api_key = api_key
        
    def analyze_content(self, text: str) -> str:
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a neutral news analyzer focusing on fact-checking and bias removal."},
                    {"role": "user", "content": text}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"OpenAI processing error: {str(e)}")
            raise

    def fact_check(self, claims: List[str]) -> Dict[str, bool]:
        results = {}
        for claim in claims:
            try:
                response = self.client.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a fact-checker. Respond with true or false."},
                        {"role": "user", "content": f"Is this claim verifiable and accurate? {claim}"}
                    ]
                )
                results[claim] = "true" in response["choices"][0]["message"]["content"].lower()
            except Exception as e:
                logger.error(f"Fact-checking error for claim '{claim}': {str(e)}")
                results[claim] = None
        return results

class GeminiProcessor(AIProcessor):
    def __init__(self, api_key: str):
        from google.genai import Client
        self.client = Client(api_key=api_key)
        self.model = "gemini-2.0-flash"
        
    def analyze_content(self, text: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[{
                    "role": "user",
                    "parts": [{
                        "text": f"Analyze this news content for neutrality and bias: {text}"
                    }]
                }]
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini processing error: {str(e)}")
            raise

    def fact_check(self, claims: List[str]) -> Dict[str, bool]:
        results = {}
        for claim in claims:
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[{
                        "role": "user",
                        "parts": [{
                            "text": f"Fact check this claim and respond with TRUE or FALSE: {claim}"
                        }]
                    }]
                )
                results[claim] = "true" in response.text.lower()
            except Exception as e:
                logger.error(f"Fact-checking error for claim '{claim}': {str(e)}")
                results[claim] = None
        return results

class NewsProcessor:
    def __init__(self, news_api_key: str, ai_processors: List[AIProcessor]):
        self.news_api = NewsAPIConfig(news_api_key)
        self.ai_processors = ai_processors
        
    def fetch_news(self, country: str = "us", category: Optional[str] = None, 
                  page_size: int = 20) -> List[Article]:
        try:
            url = f"{NewsAPIConfig.BASE_URL}/top-headlines"
            params = {
                "country": country,
                "apiKey": self.news_api.api_key,
                "pageSize": page_size
            }
            if category:
                params["category"] = category
                
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            articles_data = response.json().get("articles", [])
            return [self._create_article(article) for article in articles_data]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching news: {str(e)}")
            return []

    def _create_article(self, article_data: Dict) -> Article:
        return Article(
            title=article_data.get("title", ""),
            content=article_data.get("content", ""),
            author=article_data.get("author", ""),
            description=article_data.get("description", ""),
            url=article_data.get("url", ""),
            published_at=datetime.fromisoformat(article_data.get("publishedAt", "").replace("Z", "+00:00")),
            source_name=article_data.get("source", {}).get("name", ""),
            category=article_data.get("category", "general")
        )

    def process_article(self, article: Article) -> Article:
        try:
            # Combine analyses from multiple AI processors
            neutral_content = ""
            for processor in self.ai_processors:
                processed_content = processor.analyze_content(
                    f"{article.title} {article.content}"
                )
                neutral_content += processed_content + "\n"
            
            # Update the article content with the processed version
            article.content = neutral_content.strip()
            
            # Perform fact-checking
            claims = self._extract_claims(article.content)
            fact_check_results = {}
            
            for processor in self.ai_processors:
                processor_results = processor.fact_check(claims)
                for claim, result in processor_results.items():
                    if claim not in fact_check_results:
                        fact_check_results[claim] = result
                    else:
                        # If we have conflicting results, mark as uncertain
                        if fact_check_results[claim] != result:
                            fact_check_results[claim] = None
            
            article.fact_check_status = "verified" if all(fact_check_results.values()) else "partially_verified"
            
            return article
            
        except Exception as e:
            logger.error(f"Error processing article {article.title}: {str(e)}")
            article.fact_check_status = "error"
            return article

    def _extract_claims(self, text: str) -> List[str]:
        # This is a simplified version. In a real implementation,
        # you might want to use NLP techniques to extract claims
        sentences = text.split(". ")
        return [s.strip() + "." for s in sentences if len(s.split()) > 5]