from transformers import pipeline

def summarize_news(news_articles: str) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summaries = []
    for article in news_articles:
        summary = summarizer(article["content"], max_length=130, min_length=30, do_sample=False)
        summaries.append({
            "source": article["source"],
            "summary": summary[0]["summary_text"]
        })
    return summaries