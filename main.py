from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from news_fetcher import fetch_news
from llm_processor import summarize_news
#from chat_ai import chat_with_ai
import openai

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class NewsRequest(BaseModel):
    sources: List[str]

class NewsSummary(BaseModel):
    source: str
    summary: str

class ChatRequest(BaseModel):
    article: str
    question: str

class ChatResponse(BaseModel):
    answer: str


def chat_with_ai(article: str, question: str) -> str:
    prompt = f"Here is a news article:\n\n{article}\n\nBased on this article, answer the following question:\n{question}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assistant that answers questions based on provided news articles."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

@app.post("/summarize_news", response_model=List[NewsSummary])
async def summarize_news_endpoint(news_request: NewsRequest):
    try:
        news_articles = fetch_news(news_request.sources)
        summaries = summarize_news(news_articles)
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat_with_news", response_model=ChatResponse)
#async def chat_with_news_endpoint(chat_request: ChatRequest):
#    try:
#        answer = chat_with_ai(chat_request.article, chat_request.question)
#        return {"answer": answer}
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))

def chat_with_ai(article: str, question: str) -> str:
    prompt = f"Here is a news article:\n\n{article}\n\nBased on this article, answer the following question:\n{question}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assistant that answers questions based on provided news articles."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)