import google as genai
from google.genai import Client
import os


client = Client(api_key="AIzaSyDKjYtcoy-q0WOfreLCs0Uequg2Coe85h8")

user_q = '“Given a news article, analyze its content and fact-check its key claims using reliable sources. ' \
'Identify any misleading, exaggerated, or biased statements and provide a revised version of the article. ' \
'The new article should be written in a clear, neutral, and easy-to-understand manner, p' \
'resenting only verified facts while maintaining an objective tone. Avoid sensationalism, speculation, or political bias. ' \
'Ensure that the revised article is accessible to a general audience and free from complex jargon.”'



def revised_article(article_content: str) -> str:
    """Chats with the AI using the provided article content.

    Args:
        article_content: The content of the article.

    Returns:
        The AI's response.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            # Combine user query and article content into a single user message
            {"role": "user", "parts": [{"text": f"{user_q} Here's the article: {article_content}"}]} 
        ]
    )
    return response.text.strip()


import openai

def chat_with_openai(article_content: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    user_q = (
        "Given a news article, analyze its content and fact-check its key claims using reliable sources. "
        "Identify any misleading, exaggerated, or biased statements and provide a revised version of the article. "
        "The new article should be written in a clear, neutral, and easy-to-understand manner, "
        "presenting only verified facts while maintaining an objective tone. Avoid sensationalism, speculation, or political bias. "
        "Ensure that the revised article is accessible to a general audience and free from complex jargon."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that provides helpful answers."},
            {"role": "user", "content": user_q},
            {"role": "user", "content": article_content},
        ]
    )
    
    return response["choices"][0]["message"]["content"].strip()

# Example usage
# article_text = "Your news article here..."
# revised_article = chat_with_ai(article_text)
# print(revised_article)
