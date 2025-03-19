import google.generativeai as genai 
import os


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

user_q = '“Given a news article, analyze its content and fact-check its key claims using reliable sources. ' \
'Identify any misleading, exaggerated, or biased statements and provide a revised version of the article. ' \
'The new article should be written in a clear, neutral, and easy-to-understand manner, p' \
'resenting only verified facts while maintaining an objective tone. Avoid sensationalism, speculation, or political bias. ' \
'Ensure that the revised article is accessible to a general audience and free from complex jargon.”'



def chat_with_ai(article_content: str) -> str:

    model = genai.GenerativeModel("gemini-2.0-flash")

# Provide system instructions as part of the prompt
    response = model.generate_content(
    [
        {"role": "system", "parts": [{"text": "You are an AI assistant that provides helpful answers."}]},
        {"role": "user", "parts": [{"text": user_q}]},
        {"role": "user", "parts": [{"text": article_content}]}
    ]
    
    )
    print(response)
    return response["choices"][0]["message"]["content"].strip()


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
