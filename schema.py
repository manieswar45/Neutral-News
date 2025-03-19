from pydantic import BaseModel

class NewsArticle(BaseModel):
    source: str
    title: str
    content: str

class NewsSummary(BaseModel):
    source: str
    summary: str